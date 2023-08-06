import time #line:2
import numpy as np #line:3
import torch #line:4
import random #line:7
from collections import defaultdict #line:8
from PIL import Image #line:9
import matplotlib .pyplot as plt #line:10
import cv2 #line:11
import logging #line:14
logging .getLogger ("tensorflow").setLevel (logging .ERROR )#line:15
from .data import COLORS #line:18
from .yolact import Yolact #line:19
from .utils .augmentations import FastBaseTransform #line:20
from .utils import timer #line:21
from .utils .functions import SavePath #line:22
from .layers .output_utils import postprocess ,undo_image_transformation #line:23
from .data import cfg ,set_cfg #line:24
w_aim ,h_aim =256 ,512 #line:29
def show (OO0O0OO0O0OO0O0O0 ,size =8 ):#line:33
    plt .figure (figsize =(size ,size ))#line:34
    if np .max (OO0O0OO0O0OO0O0O0 )<=1 :#line:35
        plt .imshow (OO0O0OO0O0OO0O0O0 ,vmin =0 ,vmax =1 )#line:36
    else :#line:37
        plt .imshow (OO0O0OO0O0OO0O0O0 ,vmin =0 ,vmax =255 )#line:38
    plt .gray ()#line:39
    plt .show ()#line:40
    plt .close ()#line:41
    print ()#line:42
def make_args (argv =None ,inpass =None ,outpass =None ,model_path =None ):#line:45
    global args #line:46
    class O00O00O0000O00OOO ():#line:47
        def __init__ (O0000000000OO000O ):#line:48
            O0000000000OO000O .ap_data_file ='results/ap_data.pkl'#line:49
            O0000000000OO000O .bbox_det_file ='results/bbox_detections.json'#line:50
            O0000000000OO000O .benchmark =False #line:51
            O0000000000OO000O .config =None #line:52
            O0000000000OO000O .crop =True #line:53
            O0000000000OO000O .cuda =True #line:54
            O0000000000OO000O .dataset =None #line:55
            O0000000000OO000O .detect =False #line:56
            O0000000000OO000O .display =False #line:57
            O0000000000OO000O .display_bboxes =True #line:58
            O0000000000OO000O .display_lincomb =False #line:59
            O0000000000OO000O .display_masks =True #line:60
            O0000000000OO000O .display_scores =True #line:61
            O0000000000OO000O .display_text =True #line:62
            O0000000000OO000O .fast_nms =True #line:63
            O0000000000OO000O .image ='None:None'#line:64
            O0000000000OO000O .images =None #line:65
            O0000000000OO000O .mask_det_file ='results/mask_detections.json'#line:66
            O0000000000OO000O .mask_proto_debug =False #line:67
            O0000000000OO000O .max_images =-1 #line:68
            O0000000000OO000O .no_bar =False #line:69
            O0000000000OO000O .no_hash =False #line:70
            O0000000000OO000O .no_sort =False #line:71
            O0000000000OO000O .output_coco_json =False #line:72
            O0000000000OO000O .output_web_json =False #line:73
            O0000000000OO000O .resume =False #line:74
            O0000000000OO000O .score_threshold =0.15 #line:75
            O0000000000OO000O .seed =None #line:76
            O0000000000OO000O .shuffle =False #line:77
            O0000000000OO000O .top_k =10 #line:78
            O0000000000OO000O .trained_model =model_path #line:79
            O0000000000OO000O .video =None #line:80
            O0000000000OO000O .video_multiframe =1 #line:81
            O0000000000OO000O .web_det_path ='web/dets/'#line:82
    args =O00O00O0000O00OOO ()#line:84
    if args .output_web_json :#line:85
        args .output_coco_json =True #line:86
    if args .seed is not None :#line:88
        random .seed (args .seed )#line:89
iou_thresholds =[O0O0O0OOOO0O0O0O0 /100 for O0O0O0OOOO0O0O0O0 in range (50 ,100 ,5 )]#line:184
coco_cats ={}#line:185
coco_cats_inv ={}#line:186
color_cache =defaultdict (lambda :{})#line:187
def prep_display (O0O0O0O0O0O0000OO ,OO00O0OOOO00O0OOO ,O000OOO00O00OO0O0 ,OOO0O000OOOOOOOO0 ,OO000O0OOOO000OOO ,undo_transform =True ,class_color =False ,mask_alpha =0.45 ,w_aim =256 ,h_aim =512 ,verbose =1 ):#line:189
    ""#line:192
    if undo_transform :#line:193
        O0OO00000O0OO0OOO =undo_image_transformation (O000OOO00O00OO0O0 ,OO000O0OOOO000OOO ,OOO0O000OOOOOOOO0 )#line:194
        O0O00OOO0OOO0O000 =torch .Tensor (O0OO00000O0OO0OOO )#line:196
    else :#line:197
        O0O00OOO0OOO0O000 =O000OOO00O00OO0O0 /255.0 #line:198
        OOO0O000OOOOOOOO0 ,OO000O0OOOO000OOO ,_OO0OOO000OOO0O0OO =O000OOO00O00OO0O0 .shape #line:199
    with timer .env ('Postprocess'):#line:201
        OOOO000OO0OOO0OOO =postprocess (OO00O0OOOO00O0OOO ,OO000O0OOOO000OOO ,OOO0O000OOOOOOOO0 ,visualize_lincomb =args .display_lincomb ,crop_masks =args .crop ,score_threshold =args .score_threshold )#line:204
    with timer .env ('Copy'):#line:208
        if cfg .eval_mask_branch :#line:209
            OOOO0OOO0000OOOOO =OOOO000OO0OOO0OOO [3 ][:args .top_k ]#line:211
        O0O00000000O0O0OO ,O0OOOO0OOO000OOOO ,O0OO0OOOOO0OOOOO0 =[OOO0O0000O0OOOO0O [:args .top_k ].cpu ().numpy ()for OOO0O0000O0OOOO0O in OOOO000OO0OOO0OOO [:3 ]]#line:212
    O00O0O0O00OOOOO00 =np .array (O0O00000000O0O0OO ,str )#line:215
    O00O0O0O00OOOOO00 [O00O0O0O00OOOOO00 =='0']='person'#line:216
    O00O0O0O00OOOOO00 [O00O0O0O00OOOOO00 =='24']='backpack'#line:217
    O00O0O0O00OOOOO00 [O00O0O0O00OOOOO00 =='26']='handbag'#line:218
    O00O0O0O00OOOOO00 [O00O0O0O00OOOOO00 =='27']='tie'#line:219
    if verbose >0 :#line:220
        print ('detected: {}'.format (O00O0O0O00OOOOO00 ))#line:221
    O00OO0OO00OOO00O0 =min (args .top_k ,O0O00000000O0O0OO .shape [0 ])#line:225
    for OO00OOO000OOO00OO in range (O00OO0OO00OOO00O0 ):#line:226
        if O0OOOO0OOO000OOOO [OO00OOO000OOO00OO ]<args .score_threshold :#line:227
            O00OO0OO00OOO00O0 =OO00OOO000OOO00OO #line:228
            break #line:229
    if O00OO0OO00OOO00O0 ==0 :#line:236
        OO000O00OOOOO0O00 =np .ones ((h_aim ,w_aim ),'uint8')*255 #line:237
        return OO000O00OOOOO0O00 #line:238
    def OO0O0OO0OO000OOOO (OOOO0OO00O00O00OO ,on_gpu =None ):#line:242
        global color_cache #line:243
        OOO0O0O00OOO000OO =(O0O00000000O0O0OO [OOOO0OO00O00O00OO ]*5 if class_color else OOOO0OO00O00O00OO *5 )%len (COLORS )#line:244
        if on_gpu is not None and OOO0O0O00OOO000OO in color_cache [on_gpu ]:#line:246
            return color_cache [on_gpu ][OOO0O0O00OOO000OO ]#line:247
        else :#line:248
            O0000O000OO00000O =COLORS [OOO0O0O00OOO000OO ]#line:249
            if not undo_transform :#line:250
                O0000O000OO00000O =(O0000O000OO00000O [2 ],O0000O000OO00000O [1 ],O0000O000OO00000O [0 ])#line:252
            if on_gpu is not None :#line:253
                O0000O000OO00000O =torch .Tensor (O0000O000OO00000O ).to (on_gpu ).float ()/255. #line:254
                color_cache [on_gpu ][OOO0O0O00OOO000OO ]=O0000O000OO00000O #line:255
            return O0000O000OO00000O #line:259
    if args .display_masks and cfg .eval_mask_branch :#line:262
        OOOO0OOO0000OOOOO =OOOO0OOO0000OOOOO [:O00OO0OO00OOO00O0 ,:,:,None ]#line:264
        OOOO0OOO0000OOOOO =np .array (OOOO0OOO0000OOOOO )#line:267
        OOOO0OOO0000OOOOO =OOOO0OOO0000OOOOO .reshape (OOOO0OOO0000OOOOO .shape [:-1 ])#line:269
        OO0OOO000OO00OO00 =[]#line:274
        O00O000000O0O0000 =len (O0O0O0O0O0O0000OO )*len (O0O0O0O0O0O0000OO [0 ])#line:276
        OOO0O0O00000O0OO0 ,O000000OOO0OO0O00 =0 ,0 #line:278
        OOOOO0OOO0OO0OOOO =None #line:279
        for OO000O0OOO000O00O in range (len (O0O00000000O0O0OO )):#line:280
            if O0O00000000O0O0OO [OO000O0OOO000O00O ]==0 and np .sum (OOOO0OOO0000OOOOO [OO000O0OOO000O00O ,:,:])>O00O000000O0O0000 *0.15 *0.5 :#line:281
                OOO0O0O00000O0OO0 =np .sum (np .array (OOOO0OOO0000OOOOO [OO000O0OOO000O00O ]))#line:282
                if OOO0O0O00000O0OO0 >O000000OOO0OO0O00 :#line:283
                    O000000OOO0OO0O00 =OOO0O0O00000O0OO0 #line:284
                    OOOOO0OOO0OO0OOOO =OO000O0OOO000O00O #line:285
        if OOOOO0OOO0OO0OOOO is not None :#line:286
            OO0OOO000OO00OO00 .append (OOOOO0OOO0OO0OOOO )#line:287
        OOO0O0O00000O0OO0 ,O000000OOO0OO0O00 =0 ,0 #line:289
        OOOOO0OOO0OO0OOOO =None #line:290
        for OO000O0OOO000O00O in range (len (O0O00000000O0O0OO )):#line:291
            if O0O00000000O0O0OO [OO000O0OOO000O00O ]==24 and np .sum (OOOO0OOO0000OOOOO [OO000O0OOO000O00O ,:,:])>O00O000000O0O0000 *0.009 *0.5 :#line:292
                OOO0O0O00000O0OO0 =np .sum (np .array (OOOO0OOO0000OOOOO [OO000O0OOO000O00O ]))#line:293
                if OOO0O0O00000O0OO0 >O000000OOO0OO0O00 :#line:294
                    O000000OOO0OO0O00 =OOO0O0O00000O0OO0 #line:295
                    OOOOO0OOO0OO0OOOO =OO000O0OOO000O00O #line:296
        if OOOOO0OOO0OO0OOOO is not None :#line:297
            OO0OOO000OO00OO00 .append (OOOOO0OOO0OO0OOOO )#line:298
        OOO0O0O00000O0OO0 ,O000000OOO0OO0O00 =0 ,0 #line:300
        OOOOO0OOO0OO0OOOO =None #line:301
        for OO000O0OOO000O00O in range (len (O0O00000000O0O0OO )):#line:302
            if O0O00000000O0O0OO [OO000O0OOO000O00O ]==26 and np .sum (OOOO0OOO0000OOOOO [OO000O0OOO000O00O ,:,:])>O00O000000O0O0000 *0.009 *0.5 :#line:303
                OOO0O0O00000O0OO0 =np .sum (np .array (OOOO0OOO0000OOOOO [OO000O0OOO000O00O ]))#line:304
                if OOO0O0O00000O0OO0 >O000000OOO0OO0O00 :#line:305
                    O000000OOO0OO0O00 =OOO0O0O00000O0OO0 #line:306
                    OOOOO0OOO0OO0OOOO =OO000O0OOO000O00O #line:307
        if OOOOO0OOO0OO0OOOO is not None :#line:308
            OO0OOO000OO00OO00 .append (OOOOO0OOO0OO0OOOO )#line:309
        OOO0O0O00000O0OO0 ,O000000OOO0OO0O00 =0 ,0 #line:311
        OOOOO0OOO0OO0OOOO =None #line:312
        for OO000O0OOO000O00O in range (len (O0O00000000O0O0OO )):#line:313
            if O0O00000000O0O0OO [OO000O0OOO000O00O ]==27 and np .sum (OOOO0OOO0000OOOOO [OO000O0OOO000O00O ,:,:])>O00O000000O0O0000 *0.0025 *0.5 :#line:314
                OOO0O0O00000O0OO0 =np .sum (np .array (OOOO0OOO0000OOOOO [OO000O0OOO000O00O ]))#line:315
                if OOO0O0O00000O0OO0 >O000000OOO0OO0O00 :#line:316
                    O000000OOO0OO0O00 =OOO0O0O00000O0OO0 #line:317
                    OOOOO0OOO0OO0OOOO =OO000O0OOO000O00O #line:318
        if OOOOO0OOO0OO0OOOO is not None :#line:319
            OO0OOO000OO00OO00 .append (OOOOO0OOO0OO0OOOO )#line:320
        if verbose >0 :#line:324
            print ('valid index: {}'.format (OO0OOO000OO00OO00 ))#line:325
        if len (OO0OOO000OO00OO00 )==0 :#line:328
            OO000O00OOOOO0O00 =np .ones ((h_aim ,w_aim ,3 ),'uint8')*255 #line:329
            return OO000O00OOOOO0O00 #line:330
        OOOO0OOO0000OOOOO =OOOO0OOO0000OOOOO [OO0OOO000OO00OO00 ]#line:336
        OOO0OOOOO0O0O0O0O =np .max (OOOO0OOO0000OOOOO ,axis =0 )#line:340
        O00O000000O0O000O =np .ones ((5 ,5 ),np .uint8 )#line:364
        O0O0O0O000OOOO0OO =cv2 .morphologyEx (OOO0OOOOO0O0O0O0O ,cv2 .MORPH_CLOSE ,O00O000000O0O000O )#line:365
        O0O0O0O000OOOO0OO =np .array (O0O0O0O000OOOO0OO ,'uint8')#line:367
        try :#line:370
            _OO0OOO000OOO0O0OO ,OO00O0000OOO00O0O ,_OO0OOO000OOO0O0OO =cv2 .findContours (O0O0O0O000OOOO0OO ,cv2 .RETR_EXTERNAL ,cv2 .CHAIN_APPROX_SIMPLE )#line:371
        except :#line:372
            OO00O0000OOO00O0O ,_OO0OOO000OOO0O0OO =cv2 .findContours (O0O0O0O000OOOO0OO ,cv2 .RETR_EXTERNAL ,cv2 .CHAIN_APPROX_SIMPLE )#line:373
        OO0OOO0O00OO00O0O =max (OO00O0000OOO00O0O ,key =lambda OOO00OOO0O00OOO0O :cv2 .contourArea (OOO00OOO0O00OOO0O ))#line:376
        OO0O00OO0O00OO0O0 =np .zeros_like (O0O0O0O000OOOO0OO )#line:379
        OOO00000000OOO0OO =cv2 .drawContours (OO0O00OO0O00OO0O0 ,[OO0OOO0O00OO00O0O ],-1 ,color =255 ,thickness =-1 )#line:380
        OOOOOOOO0O000000O =np .min (np .where (OOO00000000OOO0OO >0 )[0 ])#line:384
        OO00O0O0O0000O0O0 =np .max (np .where (OOO00000000OOO0OO >0 )[0 ])#line:385
        OO0OO000OOO0OO0OO =np .min (np .where (OOO00000000OOO0OO >0 )[1 ])#line:386
        O000O0OOOOO0000O0 =np .max (np .where (OOO00000000OOO0OO >0 )[1 ])#line:387
        O0O0O0O0O0O0000OO [:,:,0 ][OOO00000000OOO0OO ==0 ]=255 #line:391
        O0O0O0O0O0O0000OO [:,:,1 ][OOO00000000OOO0OO ==0 ]=255 #line:392
        O0O0O0O0O0O0000OO [:,:,2 ][OOO00000000OOO0OO ==0 ]=255 #line:393
        O000OOO00O00OO0O0 =cv2 .cvtColor (O0O0O0O0O0O0000OO ,cv2 .COLOR_BGR2RGB )#line:397
        O000OOO00O00OO0O0 =Image .fromarray (O000OOO00O00OO0O0 )#line:398
        O000OOO00O00OO0O0 =O000OOO00O00OO0O0 .crop ((OO0OO000OOO0OO0OO ,OOOOOOOO0O000000O ,O000O0OOOOO0000O0 ,OO00O0O0O0000O0O0 ))#line:405
        OO000O0OOOO000OOO ,OOO0O000OOOOOOOO0 =O000OOO00O00OO0O0 .size #line:406
        O0000OOO00000O0OO =int (h_aim *0.95 )#line:409
        O000OOO00O00OO0O0 =O000OOO00O00OO0O0 .resize ((int (OO000O0OOOO000OOO *O0000OOO00000O0OO /OOO0O000OOOOOOOO0 ),O0000OOO00000O0OO ),Image .BICUBIC )#line:410
        OO000O0OOOO000OOO ,OOO0O000OOOOOOOO0 =O000OOO00O00OO0O0 .size #line:411
        O0OO00OO00O0000O0 =Image .new ('RGB',(w_aim ,h_aim ),(255 ,255 ,255 ))#line:415
        O0OO00OO00O0000O0 .paste (O000OOO00O00OO0O0 ,(w_aim //2 -OO000O0OOOO000OOO //2 ,int (h_aim *0.03 )))#line:416
        return O0OO00OO00O0000O0 #line:422
    return O0OO00000O0OO0OOO #line:474
def evalimage (O0000O0O000000000 ,OOOO00O0OOO000O00 :Yolact ,OO0000OO0O00O0O0O :str ,save_path :str =None ,w_aim =256 ,h_aim =512 ,verbose =1 ):#line:478
    OOOO000O00O0O00OO =torch .from_numpy (O0000O0O000000000 ).float ()#line:480
    O0O0OOOO0000O0O0O =FastBaseTransform ()(OOOO000O00O0O00OO .unsqueeze (0 ))#line:481
    OOO0OOOOO00OOO0O0 =OOOO00O0OOO000O00 (O0O0OOOO0000O0O0O )#line:482
    OO0O000O0O000O000 =prep_display (O0000O0O000000000 ,OOO0OOOOO00OOO0O0 ,OOOO000O00O0O00OO ,None ,None ,undo_transform =False ,w_aim =w_aim ,h_aim =h_aim ,verbose =verbose )#line:485
    return OO0O000O0O000O000 #line:491
def evaluate (O0O00000OOO0OOOO0 :Yolact ,O0O000OO000OO000O ,O00000OO0OO000O0O ,train_mode =False ,w_aim =256 ,h_aim =512 ,verbose =1 ):#line:496
    O0O00000OOO0OOOO0 .detect .use_fast_nms =args .fast_nms #line:497
    cfg .mask_proto_debug =args .mask_proto_debug #line:498
    OO0OO0OO0O0O0O0O0 ,OOOOOOOOO0O00O000 =args .image .split (':')#line:500
    O0OO0OO000O0OO00O =evalimage (O00000OO0OO000O0O ,O0O00000OOO0OOOO0 ,OO0OO0OO0O0O0O0O0 ,OOOOOOOOO0O00O000 ,w_aim =w_aim ,h_aim =h_aim ,verbose =verbose )#line:501
    return O0OO0OO000O0OO00O #line:502
class tool_mask :#line:538
    def __init__ (O00OOOOOOO0OO0O0O ,O0000O0OOO0OOOOO0 ,verbose =1 ):#line:539
        O00OOOOOOO0OO0O0O .verbose =verbose #line:540
        make_args (model_path =O0000O0OOO0OOOOO0 )#line:543
        if args .config is None :#line:545
            args .config ='yolact_resnet50_config'#line:550
            set_cfg (args .config )#line:552
        with torch .no_grad ():#line:554
            if O00OOOOOOO0OO0O0O .verbose >0 :#line:557
                print ('Loading mask model...',end ='')#line:558
                O0O00OOO0O0O0OOOO =time .time ()#line:559
            O00OOOOOOO0OO0O0O .net =Yolact ()#line:560
            O00OOOOOOO0OO0O0O .net .load_weights (args .trained_model )#line:561
            O00OOOOOOO0OO0O0O .net .eval ()#line:563
            if O00OOOOOOO0OO0O0O .verbose >0 :#line:564
                O00000O0O0OO0OO0O =time .time ()#line:565
                print ('Done.({}s)'.format (round (O00000O0O0OO0OO0O -O0O00OOO0O0O0OOOO ,2 )))#line:566
            if args .cuda :#line:568
                O00OOOOOOO0OO0O0O .net =O00OOOOOOO0OO0O0O .net #line:570
    def __del__ (O0OO00O0OO00OO00O ):#line:574
        pass #line:575
    def do_mask (O0OO0000O00OOO0O0 ,O0OOOOOOOO0O00O0O ,w_aim =256 ,h_aim =512 ):#line:578
        if O0OO0000O00OOO0O0 .verbose >0 :#line:581
            O0OO0OOO0OOOOOOO0 =time .time ()#line:582
        O0OOOOOOOO0O00O0O =cv2 .cvtColor (O0OOOOOOOO0O00O0O ,cv2 .COLOR_RGB2BGR )#line:585
        with torch .no_grad ():#line:587
            OO0O00O0OOO0OOO0O =None #line:589
            OOOOOOOO000000OO0 =evaluate (O0OO0000O00OOO0O0 .net ,OO0O00O0OOO0OOO0O ,O0OOOOOOOO0O00O0O ,w_aim =w_aim ,h_aim =h_aim ,verbose =O0OO0000O00OOO0O0 .verbose )#line:591
        if O0OO0000O00OOO0O0 .verbose >0 :#line:595
            OO00OOO0OOOOOO000 =time .time ()#line:596
            print ('mask end.({}s)'.format (round (OO00OOO0OOOOOO000 -O0OO0OOO0OOOOOOO0 ,2 )))#line:597
        return np .array (OOOOOOOO000000OO0 ,'uint8')#line:598
if __name__ =='__main__':#line:602
    pass #line:604
