import torch ,torchvision #line:2
import torch .nn as nn #line:3
import torch .nn .functional as F #line:4
from torchvision .models .resnet import Bottleneck #line:5
import numpy as np #line:6
from itertools import product #line:7
from math import sqrt #line:8
from typing import List #line:9
from .data .config import cfg ,mask_type #line:12
from .layers import Detect #line:13
from .layers .interpolate import InterpolateModule #line:14
from .backbone import construct_backbone #line:15
from .utils import timer #line:16
from .utils .functions import MovingAverage #line:17
ScriptModuleWrapper =nn .Module #line:30
script_method_wrapper =lambda O0OOOOO000O00OO0O ,_rcn =None :O0OOOOO000O00OO0O #line:31
class Concat (nn .Module ):#line:35
    def __init__ (O0000OO0OOO0O0OOO ,O0OOOO0O0OO0O0O00 ,O00OO00O0O00O0OO0 ):#line:36
        super ().__init__ ()#line:37
        O0000OO0OOO0O0OOO .nets =nn .ModuleList (O0OOOO0O0OO0O0O00 )#line:39
        O0000OO0OOO0O0OOO .extra_params =O00OO00O0O00O0OO0 #line:40
    def forward (O0O0O0O0O0O00OO0O ,OOOO000OO0OO00O0O ):#line:42
        return torch .cat ([OOOO0000O00OOOO0O (OOOO000OO0OO00O0O )for OOOO0000O00OOOO0O in O0O0O0O0O0O00OO0O .nets ],dim =1 ,**O0O0O0O0O0O00OO0O .extra_params )#line:44
def make_net (O00O0OOO0O000O0O0 ,O0OOOO0O00O000O00 ,include_last_relu =True ):#line:48
    ""#line:52
    def OO0OOO000O0OO00OO (O000O0OOOOOO00OO0 ):#line:53
        nonlocal O00O0OOO0O000O0O0 #line:54
        if isinstance (O000O0OOOOOO00OO0 [0 ],str ):#line:64
            OO0O0O000O00O0O0O =O000O0OOOOOO00OO0 [0 ]#line:65
            if OO0O0O000O00O0O0O =='cat':#line:67
                O00OOO000OO0O00OO =[make_net (O00O0OOO0O000O0O0 ,OOO00OO0OOO00OOOO )for OOO00OO0OOO00OOOO in O000O0OOOOOO00OO0 [1 ]]#line:68
                O00O000O0O0OO0OOO =Concat ([OOO0000O0OO000000 [0 ]for OOO0000O0OO000000 in O00OOO000OO0O00OO ],O000O0OOOOOO00OO0 [2 ])#line:69
                OOOO0000000OOOO00 =sum ([O0O00OO00O00O00OO [1 ]for O0O00OO00O00O00OO in O00OOO000OO0O00OO ])#line:70
        else :#line:71
            OOOO0000000OOOO00 =O000O0OOOOOO00OO0 [0 ]#line:72
            O00O0O0000OOOO000 =O000O0OOOOOO00OO0 [1 ]#line:73
            if O00O0O0000OOOO000 >0 :#line:75
                O00O000O0O0OO0OOO =nn .Conv2d (O00O0OOO0O000O0O0 ,OOOO0000000OOOO00 ,O00O0O0000OOOO000 ,**O000O0OOOOOO00OO0 [2 ])#line:76
            else :#line:77
                if OOOO0000000OOOO00 is None :#line:78
                    O00O000O0O0OO0OOO =InterpolateModule (scale_factor =-O00O0O0000OOOO000 ,mode ='bilinear',align_corners =False ,**O000O0OOOOOO00OO0 [2 ])#line:79
                else :#line:80
                    O00O000O0O0OO0OOO =nn .ConvTranspose2d (O00O0OOO0O000O0O0 ,OOOO0000000OOOO00 ,-O00O0O0000OOOO000 ,**O000O0OOOOOO00OO0 [2 ])#line:81
        O00O0OOO0O000O0O0 =OOOO0000000OOOO00 if OOOO0000000OOOO00 is not None else O00O0OOO0O000O0O0 #line:83
        return [O00O000O0O0OO0OOO ,nn .ReLU (inplace =True )]#line:91
    OOOO0O0OO00OO00O0 =sum ([OO0OOO000O0OO00OO (OOOOO000O0O0OO000 )for OOOOO000O0O0OO000 in O0OOOO0O00O000O00 ],[])#line:94
    if not include_last_relu :#line:95
        OOOO0O0OO00OO00O0 =OOOO0O0OO00OO00O0 [:-1 ]#line:96
    return nn .Sequential (*(OOOO0O0OO00OO00O0 )),O00O0OOO0O000O0O0 #line:98
class PredictionModule (nn .Module ):#line:102
    ""#line:126
    def __init__ (O000OOO0O0O000OO0 ,O00OO0OOOO0O00OOO ,out_channels =1024 ,aspect_ratios =[[1 ]],scales =[1 ],parent =None ):#line:128
        super ().__init__ ()#line:129
        O000OOO0O0O000OO0 .num_classes =cfg .num_classes #line:131
        O000OOO0O0O000OO0 .mask_dim =cfg .mask_dim #line:132
        O000OOO0O0O000OO0 .num_priors =sum (len (OOO000OOOOO00O0O0 )for OOO000OOOOO00O0O0 in aspect_ratios )#line:133
        O000OOO0O0O000OO0 .parent =[parent ]#line:134
        if cfg .mask_proto_prototypes_as_features :#line:136
            O00OO0OOOO0O00OOO +=O000OOO0O0O000OO0 .mask_dim #line:137
        if parent is None :#line:139
            if cfg .extra_head_net is None :#line:140
                out_channels =O00OO0OOOO0O00OOO #line:141
            else :#line:142
                O000OOO0O0O000OO0 .upfeature ,out_channels =make_net (O00OO0OOOO0O00OOO ,cfg .extra_head_net )#line:143
            if cfg .use_prediction_module :#line:145
                O000OOO0O0O000OO0 .block =Bottleneck (out_channels ,out_channels //4 )#line:146
                O000OOO0O0O000OO0 .conv =nn .Conv2d (out_channels ,out_channels ,kernel_size =1 ,bias =True )#line:147
                O000OOO0O0O000OO0 .bn =nn .BatchNorm2d (out_channels )#line:148
            O000OOO0O0O000OO0 .bbox_layer =nn .Conv2d (out_channels ,O000OOO0O0O000OO0 .num_priors *4 ,**cfg .head_layer_params )#line:150
            O000OOO0O0O000OO0 .conf_layer =nn .Conv2d (out_channels ,O000OOO0O0O000OO0 .num_priors *O000OOO0O0O000OO0 .num_classes ,**cfg .head_layer_params )#line:151
            O000OOO0O0O000OO0 .mask_layer =nn .Conv2d (out_channels ,O000OOO0O0O000OO0 .num_priors *O000OOO0O0O000OO0 .mask_dim ,**cfg .head_layer_params )#line:152
            if cfg .use_instance_coeff :#line:154
                O000OOO0O0O000OO0 .inst_layer =nn .Conv2d (out_channels ,O000OOO0O0O000OO0 .num_priors *cfg .num_instance_coeffs ,**cfg .head_layer_params )#line:155
            def OOOOO00000000OOOO (O00O0OO0000OOO0O0 ):#line:158
                if O00O0OO0000OOO0O0 ==0 :#line:159
                    return lambda O0OO0O0OOO0OOOOO0 :O0OO0O0OOO0OOOOO0 #line:160
                else :#line:161
                    return nn .Sequential (*sum ([[nn .Conv2d (out_channels ,out_channels ,kernel_size =3 ,padding =1 ),nn .ReLU (inplace =True )]for _O0OOO00OOO0O000OO in range (O00O0OO0000OOO0O0 )],[]))#line:166
            O000OOO0O0O000OO0 .bbox_extra ,O000OOO0O0O000OO0 .conf_extra ,O000OOO0O0O000OO0 .mask_extra =[OOOOO00000000OOOO (O00O0000000O0OOOO )for O00O0000000O0OOOO in cfg .extra_layers ]#line:168
            if cfg .mask_type ==mask_type .lincomb and cfg .mask_proto_coeff_gate :#line:170
                O000OOO0O0O000OO0 .gate_layer =nn .Conv2d (out_channels ,O000OOO0O0O000OO0 .num_priors *O000OOO0O0O000OO0 .mask_dim ,kernel_size =3 ,padding =1 )#line:171
        O000OOO0O0O000OO0 .aspect_ratios =aspect_ratios #line:173
        O000OOO0O0O000OO0 .scales =scales #line:174
        O000OOO0O0O000OO0 .priors =None #line:176
        O000OOO0O0O000OO0 .last_conv_size =None #line:177
    def forward (OO00O0O000OO0O0OO ,OO0OOO00OO0OO0000 ):#line:179
        ""#line:190
        OO0000O0O0OO0OO0O =OO00O0O000OO0O0OO if OO00O0O000OO0O0OO .parent [0 ]is None else OO00O0O000OO0O0OO .parent [0 ]#line:192
        OO000OOO0O0OOO0OO =OO0OOO00OO0OO0000 .size (2 )#line:194
        O0000O0OOO0OOO000 =OO0OOO00OO0OO0000 .size (3 )#line:195
        if cfg .extra_head_net is not None :#line:197
            OO0OOO00OO0OO0000 =OO0000O0O0OO0OO0O .upfeature (OO0OOO00OO0OO0000 )#line:198
        if cfg .use_prediction_module :#line:200
            OO00OO00OOOO00O00 =OO0000O0O0OO0OO0O .block (OO0OOO00OO0OO0000 )#line:202
            OOOO00OO0OOO0O0O0 =OO0000O0O0OO0OO0O .conv (OO0OOO00OO0OO0000 )#line:204
            OOOO00OO0OOO0O0O0 =OO0000O0O0OO0OO0O .bn (OOOO00OO0OOO0O0O0 )#line:205
            OOOO00OO0OOO0O0O0 =F .relu (OOOO00OO0OOO0O0O0 )#line:206
            OO0OOO00OO0OO0000 =OO00OO00OOOO00O00 +OOOO00OO0OOO0O0O0 #line:209
        O0O000000OOOOO000 =OO0000O0O0OO0OO0O .bbox_extra (OO0OOO00OO0OO0000 )#line:211
        OOOOO0OOO0O0O0O0O =OO0000O0O0OO0OO0O .conf_extra (OO0OOO00OO0OO0000 )#line:212
        O000O0O000OOO0O0O =OO0000O0O0OO0OO0O .mask_extra (OO0OOO00OO0OO0000 )#line:213
        O00O00O0OO0000O00 =OO0000O0O0OO0OO0O .bbox_layer (O0O000000OOOOO000 ).permute (0 ,2 ,3 ,1 ).contiguous ().view (OO0OOO00OO0OO0000 .size (0 ),-1 ,4 )#line:215
        O0O0O0OO0000OO000 =OO0000O0O0OO0OO0O .conf_layer (OOOOO0OOO0O0O0O0O ).permute (0 ,2 ,3 ,1 ).contiguous ().view (OO0OOO00OO0OO0000 .size (0 ),-1 ,OO00O0O000OO0O0OO .num_classes )#line:216
        if cfg .eval_mask_branch :#line:217
            O00000O00O0000OOO =OO0000O0O0OO0OO0O .mask_layer (O000O0O000OOO0O0O ).permute (0 ,2 ,3 ,1 ).contiguous ().view (OO0OOO00OO0OO0000 .size (0 ),-1 ,OO00O0O000OO0O0OO .mask_dim )#line:218
        else :#line:219
            O00000O00O0000OOO =torch .zeros (OO0OOO00OO0OO0000 .size (0 ),O00O00O0OO0000O00 .size (1 ),OO00O0O000OO0O0OO .mask_dim ,device =O00O00O0OO0000O00 .device )#line:220
        if cfg .use_instance_coeff :#line:222
            O0OO0O00OOO0O0OO0 =OO0000O0O0OO0OO0O .inst_layer (OO0OOO00OO0OO0000 ).permute (0 ,2 ,3 ,1 ).contiguous ().view (OO0OOO00OO0OO0000 .size (0 ),-1 ,cfg .num_instance_coeffs )#line:223
        if cfg .use_yolo_regressors :#line:226
            O00O00O0OO0000O00 [:,:,:2 ]=torch .sigmoid (O00O00O0OO0000O00 [:,:,:2 ])-0.5 #line:227
            O00O00O0OO0000O00 [:,:,0 ]/=O0000O0OOO0OOO000 #line:228
            O00O00O0OO0000O00 [:,:,1 ]/=OO000OOO0O0OOO0OO #line:229
        if cfg .eval_mask_branch :#line:231
            if cfg .mask_type ==mask_type .direct :#line:232
                O00000O00O0000OOO =torch .sigmoid (O00000O00O0000OOO )#line:233
            elif cfg .mask_type ==mask_type .lincomb :#line:234
                O00000O00O0000OOO =cfg .mask_proto_coeff_activation (O00000O00O0000OOO )#line:235
                if cfg .mask_proto_coeff_gate :#line:237
                    O000O000OOOOOO0O0 =OO0000O0O0OO0OO0O .gate_layer (OO0OOO00OO0OO0000 ).permute (0 ,2 ,3 ,1 ).contiguous ().view (OO0OOO00OO0OO0000 .size (0 ),-1 ,OO00O0O000OO0O0OO .mask_dim )#line:238
                    O00000O00O0000OOO =O00000O00O0000OOO *torch .sigmoid (O000O000OOOOOO0O0 )#line:239
        OO0000O0000OOO000 =OO00O0O000OO0O0OO .make_priors (OO000OOO0O0OOO0OO ,O0000O0OOO0OOO000 )#line:241
        OOO0O0OO000O0O0O0 ={'loc':O00O00O0OO0000O00 ,'conf':O0O0O0OO0000OO000 ,'mask':O00000O00O0000OOO ,'priors':OO0000O0000OOO000 }#line:243
        if cfg .use_instance_coeff :#line:245
            OOO0O0OO000O0O0O0 ['inst']=O0OO0O00OOO0O0OO0 #line:246
        return OOO0O0OO000O0O0O0 #line:248
    def make_priors (O0O000000O0000000 ,OOO0O0OOO0OOO0OO0 ,OO00O0O0O0OO000O0 ):#line:250
        ""#line:251
        with timer .env ('makepriors'):#line:253
            if O0O000000O0000000 .last_conv_size !=(OO00O0O0O0OO000O0 ,OOO0O0OOO0OOO0OO0 ):#line:254
                OO000O0OO0O0OOO0O =[]#line:255
                for OOOO00O00000OO00O ,OOOOO0O00O00OOOO0 in product (range (OOO0O0OOO0OOO0OO0 ),range (OO00O0O0O0OO000O0 )):#line:258
                    O00O00OO0OO000OO0 =(OOOOO0O00O00OOOO0 +0.5 )/OO00O0O0O0OO000O0 #line:260
                    O00O0OO0OOO0OOO0O =(OOOO00O00000OO00O +0.5 )/OOO0O0OOO0OOO0OO0 #line:261
                    for O00O000O0OOO0000O ,OOO0OOOOO0O0OO00O in zip (O0O000000O0000000 .scales ,O0O000000O0000000 .aspect_ratios ):#line:263
                        for OOO0OO00OOOO0OO0O in OOO0OOOOO0O0OO00O :#line:264
                            if not cfg .backbone .preapply_sqrt :#line:265
                                OOO0OO00OOOO0OO0O =sqrt (OOO0OO00OOOO0OO0O )#line:266
                            if cfg .backbone .use_pixel_scales :#line:268
                                O0O000O00OO0OOO00 =O00O000O0OOO0000O *OOO0OO00OOOO0OO0O /cfg .max_size #line:269
                                O0000OO0OOOOOOOOO =O00O000O0OOO0000O *OOO0OO00OOOO0OO0O /cfg .max_size #line:271
                            else :#line:272
                                O0O000O00OO0OOO00 =O00O000O0OOO0000O *OOO0OO00OOOO0OO0O /OO00O0O0O0OO000O0 #line:273
                                O0000OO0OOOOOOOOO =O00O000O0OOO0000O /OOO0OO00OOOO0OO0O /OOO0O0OOO0OOO0OO0 #line:274
                            OO000O0OO0O0OOO0O +=[O00O00OO0OO000OO0 ,O00O0OO0OOO0OOO0O ,O0O000O00OO0OOO00 ,O0000OO0OOOOOOOOO ]#line:276
                O0O000000O0000000 .priors =torch .Tensor (OO000O0OO0O0OOO0O ).view (-1 ,4 )#line:278
                O0O000000O0000000 .last_conv_size =(OO00O0O0O0OO000O0 ,OOO0O0OOO0OOO0OO0 )#line:279
        return O0O000000O0000000 .priors #line:281
class FPN (ScriptModuleWrapper ):#line:283
    ""#line:297
    __constants__ =['interpolation_mode','num_downsample','use_conv_downsample','lat_layers','pred_layers','downsample_layers']#line:299
    def __init__ (O0OOO0OOOO0OO00OO ,OO000OO0000OO00O0 ):#line:301
        super ().__init__ ()#line:302
        O0OOO0OOOO0OO00OO .lat_layers =nn .ModuleList ([nn .Conv2d (O0O00O00OO00O0O0O ,cfg .fpn .num_features ,kernel_size =1 )for O0O00O00OO00O0O0O in reversed (OO000OO0000OO00O0 )])#line:307
        O00O000OO0OO0OOO0 =1 if cfg .fpn .pad else 0 #line:310
        O0OOO0OOOO0OO00OO .pred_layers =nn .ModuleList ([nn .Conv2d (cfg .fpn .num_features ,cfg .fpn .num_features ,kernel_size =3 ,padding =O00O000OO0OO0OOO0 )for _O00OO00O000O0OOOO in OO000OO0000OO00O0 ])#line:314
        if cfg .fpn .use_conv_downsample :#line:316
            O0OOO0OOOO0OO00OO .downsample_layers =nn .ModuleList ([nn .Conv2d (cfg .fpn .num_features ,cfg .fpn .num_features ,kernel_size =3 ,padding =1 ,stride =2 )for _O00O0OO0O000OO00O in range (cfg .fpn .num_downsample )])#line:320
        O0OOO0OOOO0OO00OO .interpolation_mode =cfg .fpn .interpolation_mode #line:322
        O0OOO0OOOO0OO00OO .num_downsample =cfg .fpn .num_downsample #line:323
        O0OOO0OOOO0OO00OO .use_conv_downsample =cfg .fpn .use_conv_downsample #line:324
    @script_method_wrapper #line:326
    def forward (O0OOOO00OO0OO00OO ,OOO00O0000O000OOO :List [torch .Tensor ]):#line:327
        ""#line:333
        O00OOO0000000OOOO =[]#line:335
        OOOOOOOO0O0OO0OOO =torch .zeros (1 ,device =OOO00O0000O000OOO [0 ].device )#line:336
        for OOOO00OO000O0O0O0 in range (len (OOO00O0000O000OOO )):#line:337
            O00OOO0000000OOOO .append (OOOOOOOO0O0OO0OOO )#line:338
        OOO0OO0O0OO0OOOO0 =len (OOO00O0000O000OOO )#line:342
        for OO00O0O00OOO0OOOO in O0OOOO00OO0OO00OO .lat_layers :#line:343
            OOO0OO0O0OO0OOOO0 -=1 #line:344
            if OOO0OO0O0OO0OOOO0 <len (OOO00O0000O000OOO )-1 :#line:346
                _OO00OO0O0O0O0OOOO ,_OO00OO0O0O0O0OOOO ,O0OO0OO00O00O0000 ,OOO00O000O00OO000 =OOO00O0000O000OOO [OOO0OO0O0OO0OOOO0 ].size ()#line:347
                OOOOOOOO0O0OO0OOO =F .interpolate (OOOOOOOO0O0OO0OOO ,size =(O0OO0OO00O00O0000 ,OOO00O000O00OO000 ),mode =O0OOOO00OO0OO00OO .interpolation_mode ,align_corners =False )#line:348
            OOOOOOOO0O0OO0OOO =OOOOOOOO0O0OO0OOO +OO00O0O00OOO0OOOO (OOO00O0000O000OOO [OOO0OO0O0OO0OOOO0 ])#line:350
            O00OOO0000000OOOO [OOO0OO0O0OO0OOOO0 ]=OOOOOOOO0O0OO0OOO #line:351
        OOO0OO0O0OO0OOOO0 =len (OOO00O0000O000OOO )#line:354
        for O0O0OOO0O0O0O0OO0 in O0OOOO00OO0OO00OO .pred_layers :#line:355
            OOO0OO0O0OO0OOOO0 -=1 #line:356
            O00OOO0000000OOOO [OOO0OO0O0OO0OOOO0 ]=F .relu (O0O0OOO0O0O0O0OO0 (O00OOO0000000OOOO [OOO0OO0O0OO0OOOO0 ]))#line:357
        if O0OOOO00OO0OO00OO .use_conv_downsample :#line:360
            for OOOOOO000OOOOO0OO in O0OOOO00OO0OO00OO .downsample_layers :#line:361
                O00OOO0000000OOOO .append (OOOOOO000OOOOO0OO (O00OOO0000000OOOO [-1 ]))#line:362
        else :#line:363
            for OO000O00OO0O0000O in range (O0OOOO00OO0OO00OO .num_downsample ):#line:364
                O00OOO0000000OOOO .append (nn .functional .max_pool2d (O00OOO0000000OOOO [-1 ],1 ,stride =2 ))#line:366
        return O00OOO0000000OOOO #line:368
class Yolact (nn .Module ):#line:372
    ""#line:390
    def __init__ (OO0O0OO0OO0OOOOOO ):#line:392
        super ().__init__ ()#line:393
        OO0O0OO0OO0OOOOOO .backbone =construct_backbone (cfg .backbone )#line:395
        if cfg .freeze_bn :#line:397
            OO0O0OO0OO0OOOOOO .freeze_bn ()#line:398
        if cfg .mask_type ==mask_type .direct :#line:401
            cfg .mask_dim =cfg .mask_size **2 #line:402
        elif cfg .mask_type ==mask_type .lincomb :#line:403
            if cfg .mask_proto_use_grid :#line:404
                OO0O0OO0OO0OOOOOO .grid =torch .Tensor (np .load (cfg .mask_proto_grid_file ))#line:405
                OO0O0OO0OO0OOOOOO .num_grids =OO0O0OO0OO0OOOOOO .grid .size (0 )#line:406
            else :#line:407
                OO0O0OO0OO0OOOOOO .num_grids =0 #line:408
            OO0O0OO0OO0OOOOOO .proto_src =cfg .mask_proto_src #line:410
            if OO0O0OO0OO0OOOOOO .proto_src is None :O0OO00O0O0OOOOOOO =3 #line:412
            elif cfg .fpn is not None :O0OO00O0O0OOOOOOO =cfg .fpn .num_features #line:413
            else :O0OO00O0O0OOOOOOO =OO0O0OO0OO0OOOOOO .backbone .channels [OO0O0OO0OO0OOOOOO .proto_src ]#line:414
            O0OO00O0O0OOOOOOO +=OO0O0OO0OO0OOOOOO .num_grids #line:415
            OO0O0OO0OO0OOOOOO .proto_net ,cfg .mask_dim =make_net (O0OO00O0O0OOOOOOO ,cfg .mask_proto_net ,include_last_relu =False )#line:418
            if cfg .mask_proto_bias :#line:420
                cfg .mask_dim +=1 #line:421
        OO0O0OO0OO0OOOOOO .selected_layers =cfg .backbone .selected_layers #line:424
        OOOO00OOO00O0O000 =OO0O0OO0OO0OOOOOO .backbone .channels #line:425
        if cfg .fpn is not None :#line:427
            OO0O0OO0OO0OOOOOO .fpn =FPN ([OOOO00OOO00O0O000 [O0O00OO00OOOO0OO0 ]for O0O00OO00OOOO0OO0 in OO0O0OO0OO0OOOOOO .selected_layers ])#line:429
            OO0O0OO0OO0OOOOOO .selected_layers =list (range (len (OO0O0OO0OO0OOOOOO .selected_layers )+cfg .fpn .num_downsample ))#line:430
            OOOO00OOO00O0O000 =[cfg .fpn .num_features ]*len (OO0O0OO0OO0OOOOOO .selected_layers )#line:431
        OO0O0OO0OO0OOOOOO .prediction_layers =nn .ModuleList ()#line:434
        for O0OOO0O0OO00O0000 ,O0OOOO0000OOOO00O in enumerate (OO0O0OO0OO0OOOOOO .selected_layers ):#line:436
            O00OOO00O0000O000 =None #line:438
            if cfg .share_prediction_module and O0OOO0O0OO00O0000 >0 :#line:439
                O00OOO00O0000O000 =OO0O0OO0OO0OOOOOO .prediction_layers [0 ]#line:440
            O0O00OO000OO00O00 =PredictionModule (OOOO00OOO00O0O000 [O0OOOO0000OOOO00O ],OOOO00OOO00O0O000 [O0OOOO0000OOOO00O ],aspect_ratios =cfg .backbone .pred_aspect_ratios [O0OOO0O0OO00O0000 ],scales =cfg .backbone .pred_scales [O0OOO0O0OO00O0000 ],parent =O00OOO00O0000O000 )#line:445
            OO0O0OO0OO0OOOOOO .prediction_layers .append (O0O00OO000OO00O00 )#line:446
        if cfg .use_class_existence_loss :#line:449
            OO0O0OO0OO0OOOOOO .class_existence_fc =nn .Linear (OOOO00OOO00O0O000 [-1 ],cfg .num_classes -1 )#line:452
        if cfg .use_semantic_segmentation_loss :#line:454
            OO0O0OO0OO0OOOOOO .semantic_seg_conv =nn .Conv2d (OOOO00OOO00O0O000 [0 ],cfg .num_classes -1 ,kernel_size =1 )#line:455
        OO0O0OO0OO0OOOOOO .detect =Detect (cfg .num_classes ,bkg_label =0 ,top_k =200 ,conf_thresh =0.05 ,nms_thresh =0.5 )#line:458
    def save_weights (O00O00O0000OO00O0 ,OOOO0O0OOOOOOO0O0 ):#line:460
        ""#line:461
        torch .save (O00O00O0000OO00O0 .state_dict (),OOOO0O0OOOOOOO0O0 )#line:462
    def load_weights (O0OOO00O0O00O00O0 ,OOO00OO00OOO0OOOO ):#line:464
        ""#line:465
        O00OO000O0OO0OO00 =torch .load (OOO00OO00OOO0OOOO ,map_location ='cpu')#line:466
        for O000O0O0O0OOO0O0O in list (O00OO000O0OO0OO00 .keys ()):#line:469
            if O000O0O0O0OOO0O0O .startswith ('backbone.layer')and not O000O0O0O0OOO0O0O .startswith ('backbone.layers'):#line:470
                del O00OO000O0OO0OO00 [O000O0O0O0OOO0O0O ]#line:471
            if O000O0O0O0OOO0O0O .startswith ('fpn.downsample_layers.'):#line:474
                if cfg .fpn is not None and int (O000O0O0O0OOO0O0O .split ('.')[2 ])>=cfg .fpn .num_downsample :#line:475
                    del O00OO000O0OO0OO00 [O000O0O0O0OOO0O0O ]#line:476
        O0OOO00O0O00O00O0 .load_state_dict (O00OO000O0OO0OO00 )#line:478
    def init_weights (O0O00OOOOO0OOOOOO ,OOO000000OO00O0O0 ):#line:480
        ""#line:481
        O0O00OOOOO0OOOOOO .backbone .init_backbone (OOO000000OO00O0O0 )#line:483
        for OOOO0O0O00000OOOO ,O0OOO0O0000OO0OOO in O0O00OOOOO0OOOOOO .named_modules ():#line:486
            if isinstance (O0OOO0O0000OO0OOO ,nn .Conv2d )and O0OOO0O0000OO0OOO not in O0O00OOOOO0OOOOOO .backbone .backbone_modules :#line:487
                nn .init .xavier_uniform_ (O0OOO0O0000OO0OOO .weight .data )#line:488
                if O0OOO0O0000OO0OOO .bias is not None :#line:490
                    if cfg .use_focal_loss and 'conf_layer'in OOOO0O0O00000OOOO :#line:491
                        if not cfg .use_sigmoid_focal_loss :#line:492
                            O0OOO0O0000OO0OOO .bias .data [0 ]=np .log ((1 -cfg .focal_loss_init_pi )/cfg .focal_loss_init_pi )#line:503
                            O0OOO0O0000OO0OOO .bias .data [1 :]=-np .log (O0OOO0O0000OO0OOO .bias .size (0 )-1 )#line:504
                        else :#line:505
                            O0OOO0O0000OO0OOO .bias .data [0 ]=-np .log (cfg .focal_loss_init_pi /(1 -cfg .focal_loss_init_pi ))#line:506
                            O0OOO0O0000OO0OOO .bias .data [1 :]=-np .log ((1 -cfg .focal_loss_init_pi )/cfg .focal_loss_init_pi )#line:507
                    else :#line:508
                        O0OOO0O0000OO0OOO .bias .data .zero_ ()#line:509
    def train (O00OO0OOO0000O00O ,mode =True ):#line:511
        super ().train (mode )#line:512
        if cfg .freeze_bn :#line:514
            O00OO0OOO0000O00O .freeze_bn ()#line:515
    def freeze_bn (O0OOOOO00000O0OOO ):#line:517
        ""#line:518
        for O000O00O0OO0O00OO in O0OOOOO00000O0OOO .modules ():#line:519
            if isinstance (O000O00O0OO0O00OO ,nn .BatchNorm2d ):#line:520
                O000O00O0OO0O00OO .eval ()#line:521
                O000O00O0OO0O00OO .weight .requires_grad =False #line:523
                O000O00O0OO0O00OO .bias .requires_grad =False #line:524
    def forward (OO0O0O00O0OOOO000 ,O000000OOOO0O0O00 ):#line:526
        ""#line:527
        with timer .env ('backbone'):#line:528
            OOO0000OOO0OOO00O =OO0O0O00O0OOOO000 .backbone (O000000OOOO0O0O00 )#line:529
        if cfg .fpn is not None :#line:531
            with timer .env ('fpn'):#line:532
                OOO0000OOO0OOO00O =[OOO0000OOO0OOO00O [O000OO00O000O000O ]for O000OO00O000O000O in cfg .backbone .selected_layers ]#line:534
                OOO0000OOO0OOO00O =OO0O0O00O0OOOO000 .fpn (OOO0000OOO0OOO00O )#line:535
        O0OO0O0O0O0000O0O =None #line:537
        if cfg .mask_type ==mask_type .lincomb and cfg .eval_mask_branch :#line:538
            with timer .env ('proto'):#line:539
                O00O0OOOOOOOOOOO0 =O000000OOOO0O0O00 if OO0O0O00O0OOOO000 .proto_src is None else OOO0000OOO0OOO00O [OO0O0O00O0OOOO000 .proto_src ]#line:540
                if OO0O0O00O0OOOO000 .num_grids >0 :#line:542
                    OO0O000OO0O0O00OO =OO0O0O00O0OOOO000 .grid .repeat (O00O0OOOOOOOOOOO0 .size (0 ),1 ,1 ,1 )#line:543
                    O00O0OOOOOOOOOOO0 =torch .cat ([O00O0OOOOOOOOOOO0 ,OO0O000OO0O0O00OO ],dim =1 )#line:544
                O0OO0O0O0O0000O0O =OO0O0O00O0OOOO000 .proto_net (O00O0OOOOOOOOOOO0 )#line:546
                O0OO0O0O0O0000O0O =cfg .mask_proto_prototype_activation (O0OO0O0O0O0000O0O )#line:547
                if cfg .mask_proto_prototypes_as_features :#line:549
                    OOOO00000OO0OO00O =O0OO0O0O0O0000O0O .clone ()#line:551
                    if cfg .mask_proto_prototypes_as_features_no_grad :#line:553
                        OOOO00000OO0OO00O =O0OO0O0O0O0000O0O .detach ()#line:554
                O0OO0O0O0O0000O0O =O0OO0O0O0O0000O0O .permute (0 ,2 ,3 ,1 ).contiguous ()#line:557
                if cfg .mask_proto_bias :#line:559
                    OOOO0OOOOO0OOOO00 =[OO0OO00O000OOOO0O for OO0OO00O000OOOO0O in O0OO0O0O0O0000O0O .size ()]#line:560
                    OOOO0OOOOO0OOOO00 [-1 ]=1 #line:561
                    O0OO0O0O0O0000O0O =torch .cat ([O0OO0O0O0O0000O0O ,torch .ones (*OOOO0OOOOO0OOOO00 )],-1 )#line:562
        with timer .env ('pred_heads'):#line:565
            OO000OOOOOOOO0OOO ={'loc':[],'conf':[],'mask':[],'priors':[]}#line:566
            if cfg .use_instance_coeff :#line:568
                OO000OOOOOOOO0OOO ['inst']=[]#line:569
            for OO0000OO0000OO000 ,OOOOO00O0O0OOOOO0 in zip (OO0O0O00O0OOOO000 .selected_layers ,OO0O0O00O0OOOO000 .prediction_layers ):#line:571
                O0OO0000OOO00O00O =OOO0000OOO0OOO00O [OO0000OO0000OO000 ]#line:572
                if cfg .mask_type ==mask_type .lincomb and cfg .mask_proto_prototypes_as_features :#line:574
                    OOOO00000OO0OO00O =F .interpolate (OOOO00000OO0OO00O ,size =OOO0000OOO0OOO00O [OO0000OO0000OO000 ].size ()[2 :],mode ='bilinear',align_corners =False )#line:576
                    O0OO0000OOO00O00O =torch .cat ([O0OO0000OOO00O00O ,OOOO00000OO0OO00O ],dim =1 )#line:577
                if cfg .share_prediction_module and OOOOO00O0O0OOOOO0 is not OO0O0O00O0OOOO000 .prediction_layers [0 ]:#line:580
                    OOOOO00O0O0OOOOO0 .parent =[OO0O0O00O0OOOO000 .prediction_layers [0 ]]#line:581
                OOO00O00O00OOO0OO =OOOOO00O0O0OOOOO0 (O0OO0000OOO00O00O )#line:583
                for O0O0000O0O0OOO0OO ,O0O00OOO0OO0O0OOO in OOO00O00O00OOO0OO .items ():#line:585
                    OO000OOOOOOOO0OOO [O0O0000O0O0OOO0OO ].append (O0O00OOO0OO0O0OOO )#line:586
        for O0O0000O0O0OOO0OO ,O0O00OOO0OO0O0OOO in OO000OOOOOOOO0OOO .items ():#line:588
            OO000OOOOOOOO0OOO [O0O0000O0O0OOO0OO ]=torch .cat (O0O00OOO0OO0O0OOO ,-2 )#line:589
        if O0OO0O0O0O0000O0O is not None :#line:591
            OO000OOOOOOOO0OOO ['proto']=O0OO0O0O0O0000O0O #line:592
        if OO0O0O00O0OOOO000 .training :#line:594
            if cfg .use_class_existence_loss :#line:597
                OO000OOOOOOOO0OOO ['classes']=OO0O0O00O0OOOO000 .class_existence_fc (OOO0000OOO0OOO00O [-1 ].mean (dim =(2 ,3 )))#line:598
            if cfg .use_semantic_segmentation_loss :#line:600
                OO000OOOOOOOO0OOO ['segm']=OO0O0O00O0OOOO000 .semantic_seg_conv (OOO0000OOO0OOO00O [0 ])#line:601
            return OO000OOOOOOOO0OOO #line:603
        else :#line:604
            if cfg .use_sigmoid_focal_loss :#line:605
                OO000OOOOOOOO0OOO ['conf']=torch .sigmoid (OO000OOOOOOOO0OOO ['conf'])#line:607
            elif cfg .use_objectness_score :#line:608
                OO00OO00OOOO0000O =torch .sigmoid (OO000OOOOOOOO0OOO ['conf'][:,:,0 ])#line:610
                OO000OOOOOOOO0OOO ['conf'][:,:,1 :]=OO00OO00OOOO0000O [:,:,None ]*F .softmax (OO000OOOOOOOO0OOO ['conf'][:,:,1 :],-1 )#line:611
                OO000OOOOOOOO0OOO ['conf'][:,:,0 ]=1 -OO00OO00OOOO0000O #line:612
            else :#line:613
                OO000OOOOOOOO0OOO ['conf']=F .softmax (OO000OOOOOOOO0OOO ['conf'],-1 )#line:614
            return OO0O0O00O0OOOO000 .detect (OO000OOOOOOOO0OOO )#line:616
if __name__ =='__main__':#line:622
    from utils .functions import init_console #line:623
    init_console ()#line:624
    import sys #line:627
    if len (sys .argv )>1 :#line:628
        from data .config import set_cfg #line:629
        set_cfg (sys .argv [1 ])#line:630
    net =Yolact ()#line:632
    net .train ()#line:633
    net .init_weights (backbone_path ='weights/'+cfg .backbone .path )#line:634
    net =net #line:638
    torch .set_default_tensor_type ('torch.FloatTensor')#line:640
    x =torch .zeros ((1 ,3 ,cfg .max_size ,cfg .max_size ))#line:642
    y =net (x )#line:643
    for p in net .prediction_layers :#line:645
        print (p .last_conv_size )#line:646
    print ()#line:648
    for k ,a in y .items ():#line:649
        print (k +': ',a .size (),torch .sum (a ))#line:650
    exit ()#line:651
    net (x )#line:653
    avg =MovingAverage ()#line:655
    try :#line:656
        while True :#line:657
            timer .reset ()#line:658
            with timer .env ('everything else'):#line:659
                net (x )#line:660
            avg .add (timer .total_time ())#line:661
            print ('\033[2J')#line:662
            timer .print_stats ()#line:663
            print ('Avg fps: %.2f\tAvg ms: %.2f         '%(1 /avg .get_avg (),avg .get_avg ()*1000 ))#line:664
    except KeyboardInterrupt :#line:665
        pass #line:666
