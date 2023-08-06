import torch #line:1
import torch .nn as nn #line:2
import pickle #line:3
from collections import OrderedDict #line:5
class Bottleneck (nn .Module ):#line:7
    ""#line:8
    expansion =4 #line:9
    def __init__ (OO00OO000O0OOOO0O ,OOOOO0OO000O0OO00 ,O00000O0000O00000 ,stride =1 ,downsample =None ,norm_layer =nn .BatchNorm2d ,dilation =1 ):#line:11
        super (Bottleneck ,OO00OO000O0OOOO0O ).__init__ ()#line:12
        OO00OO000O0OOOO0O .conv1 =nn .Conv2d (OOOOO0OO000O0OO00 ,O00000O0000O00000 ,kernel_size =1 ,bias =False ,dilation =dilation )#line:13
        OO00OO000O0OOOO0O .bn1 =norm_layer (O00000O0000O00000 )#line:14
        OO00OO000O0OOOO0O .conv2 =nn .Conv2d (O00000O0000O00000 ,O00000O0000O00000 ,kernel_size =3 ,stride =stride ,padding =dilation ,bias =False ,dilation =dilation )#line:16
        OO00OO000O0OOOO0O .bn2 =norm_layer (O00000O0000O00000 )#line:17
        OO00OO000O0OOOO0O .conv3 =nn .Conv2d (O00000O0000O00000 ,O00000O0000O00000 *4 ,kernel_size =1 ,bias =False ,dilation =dilation )#line:18
        OO00OO000O0OOOO0O .bn3 =norm_layer (O00000O0000O00000 *4 )#line:19
        OO00OO000O0OOOO0O .relu =nn .ReLU (inplace =True )#line:20
        OO00OO000O0OOOO0O .downsample =downsample #line:21
        OO00OO000O0OOOO0O .stride =stride #line:22
    def forward (O0O000O00OO0O0O00 ,O000OOOOO0OO0OOO0 ):#line:24
        OOOO00000OOO000OO =O000OOOOO0OO0OOO0 #line:25
        OOOOO0O0O00O0OOOO =O0O000O00OO0O0O00 .conv1 (O000OOOOO0OO0OOO0 )#line:27
        OOOOO0O0O00O0OOOO =O0O000O00OO0O0O00 .bn1 (OOOOO0O0O00O0OOOO )#line:28
        OOOOO0O0O00O0OOOO =O0O000O00OO0O0O00 .relu (OOOOO0O0O00O0OOOO )#line:29
        OOOOO0O0O00O0OOOO =O0O000O00OO0O0O00 .conv2 (OOOOO0O0O00O0OOOO )#line:31
        OOOOO0O0O00O0OOOO =O0O000O00OO0O0O00 .bn2 (OOOOO0O0O00O0OOOO )#line:32
        OOOOO0O0O00O0OOOO =O0O000O00OO0O0O00 .relu (OOOOO0O0O00O0OOOO )#line:33
        OOOOO0O0O00O0OOOO =O0O000O00OO0O0O00 .conv3 (OOOOO0O0O00O0OOOO )#line:35
        OOOOO0O0O00O0OOOO =O0O000O00OO0O0O00 .bn3 (OOOOO0O0O00O0OOOO )#line:36
        if O0O000O00OO0O0O00 .downsample is not None :#line:38
            OOOO00000OOO000OO =O0O000O00OO0O0O00 .downsample (O000OOOOO0OO0OOO0 )#line:39
        OOOOO0O0O00O0OOOO +=OOOO00000OOO000OO #line:41
        OOOOO0O0O00O0OOOO =O0O000O00OO0O0O00 .relu (OOOOO0O0O00O0OOOO )#line:42
        return OOOOO0O0O00O0OOOO #line:44
class ResNetBackbone (nn .Module ):#line:47
    ""#line:48
    def __init__ (O0OO000O000O0O000 ,OO000OOO00000OO0O ,atrous_layers =[],block =Bottleneck ,norm_layer =nn .BatchNorm2d ):#line:50
        super ().__init__ ()#line:51
        O0OO000O000O0O000 .num_base_layers =len (OO000OOO00000OO0O )#line:54
        O0OO000O000O0O000 .layers =nn .ModuleList ()#line:55
        O0OO000O000O0O000 .channels =[]#line:56
        O0OO000O000O0O000 .norm_layer =norm_layer #line:57
        O0OO000O000O0O000 .dilation =1 #line:58
        O0OO000O000O0O000 .atrous_layers =atrous_layers #line:59
        O0OO000O000O0O000 .inplanes =64 #line:62
        O0OO000O000O0O000 .conv1 =nn .Conv2d (3 ,64 ,kernel_size =7 ,stride =2 ,padding =3 ,bias =False )#line:64
        O0OO000O000O0O000 .bn1 =norm_layer (64 )#line:65
        O0OO000O000O0O000 .relu =nn .ReLU (inplace =True )#line:66
        O0OO000O000O0O000 .maxpool =nn .MaxPool2d (kernel_size =3 ,stride =2 ,padding =1 )#line:67
        O0OO000O000O0O000 ._make_layer (block ,64 ,OO000OOO00000OO0O [0 ])#line:69
        O0OO000O000O0O000 ._make_layer (block ,128 ,OO000OOO00000OO0O [1 ],stride =2 )#line:70
        O0OO000O000O0O000 ._make_layer (block ,256 ,OO000OOO00000OO0O [2 ],stride =2 )#line:71
        O0OO000O000O0O000 ._make_layer (block ,512 ,OO000OOO00000OO0O [3 ],stride =2 )#line:72
        O0OO000O000O0O000 .backbone_modules =[O00O00O00OO0OO0OO for O00O00O00OO0OO0OO in O0OO000O000O0O000 .modules ()if isinstance (O00O00O00OO0OO0OO ,nn .Conv2d )]#line:78
    def _make_layer (OO0O0000OO0OO0O0O ,O00O000O0000000OO ,O00O0OO0O00OO0000 ,OOO00O00O00O0OO0O ,stride =1 ):#line:81
        ""#line:82
        OO0O0O0O0OOO000OO =None #line:83
        if stride !=1 or OO0O0000OO0OO0O0O .inplanes !=O00O0OO0O00OO0000 *O00O000O0000000OO .expansion :#line:87
            if len (OO0O0000OO0OO0O0O .layers )in OO0O0000OO0OO0O0O .atrous_layers :#line:88
                OO0O0000OO0OO0O0O .dilation +=1 #line:89
                stride =1 #line:90
            OO0O0O0O0OOO000OO =nn .Sequential (nn .Conv2d (OO0O0000OO0OO0O0O .inplanes ,O00O0OO0O00OO0000 *O00O000O0000000OO .expansion ,kernel_size =1 ,stride =stride ,bias =False ,dilation =OO0O0000OO0OO0O0O .dilation ),OO0O0000OO0OO0O0O .norm_layer (O00O0OO0O00OO0000 *O00O000O0000000OO .expansion ),)#line:97
        O0OOO00O00O0OO00O =[]#line:99
        O0OOO00O00O0OO00O .append (O00O000O0000000OO (OO0O0000OO0OO0O0O .inplanes ,O00O0OO0O00OO0000 ,stride ,OO0O0O0O0OOO000OO ,OO0O0000OO0OO0O0O .norm_layer ,OO0O0000OO0OO0O0O .dilation ))#line:100
        OO0O0000OO0OO0O0O .inplanes =O00O0OO0O00OO0000 *O00O000O0000000OO .expansion #line:101
        for O0000OO0OO0OO0OO0 in range (1 ,OOO00O00O00O0OO0O ):#line:102
            O0OOO00O00O0OO00O .append (O00O000O0000000OO (OO0O0000OO0OO0O0O .inplanes ,O00O0OO0O00OO0000 ,norm_layer =OO0O0000OO0OO0O0O .norm_layer ))#line:103
        O0O00OO00OO000O00 =nn .Sequential (*O0OOO00O00O0OO00O )#line:105
        OO0O0000OO0OO0O0O .channels .append (O00O0OO0O00OO0000 *O00O000O0000000OO .expansion )#line:107
        OO0O0000OO0OO0O0O .layers .append (O0O00OO00OO000O00 )#line:108
        return O0O00OO00OO000O00 #line:110
    def forward (O0OO0O00O0000OO00 ,O0O0O000O00O00000 ):#line:112
        ""#line:113
        O0O0O000O00O00000 =O0OO0O00O0000OO00 .conv1 (O0O0O000O00O00000 )#line:115
        O0O0O000O00O00000 =O0OO0O00O0000OO00 .bn1 (O0O0O000O00O00000 )#line:116
        O0O0O000O00O00000 =O0OO0O00O0000OO00 .relu (O0O0O000O00O00000 )#line:117
        O0O0O000O00O00000 =O0OO0O00O0000OO00 .maxpool (O0O0O000O00O00000 )#line:118
        OO0O00O0O00OOOOO0 =[]#line:120
        for OO0OO0O000000OO0O in O0OO0O00O0000OO00 .layers :#line:121
            O0O0O000O00O00000 =OO0OO0O000000OO0O (O0O0O000O00O00000 )#line:122
            OO0O00O0O00OOOOO0 .append (O0O0O000O00O00000 )#line:123
        return tuple (OO0O00O0O00OOOOO0 )#line:125
    def init_backbone (O0OO0OOOO000OO0O0 ,OO0O00OO0O0O00000 ):#line:127
        ""#line:128
        OO000O0O0OOO0O0OO =torch .load (OO0O00OO0O0O00000 )#line:129
        O0O00OO00O00000O0 =list (OO000O0O0OOO0O0OO )#line:132
        for O00O00OOO00O0O00O in O0O00OO00O00000O0 :#line:133
            if O00O00OOO00O0O00O .startswith ('layer'):#line:134
                O00O00O0000O0000O =int (O00O00OOO00O0O00O [5 ])#line:135
                OOOOOOO00O0O0O0O0 ='layers.'+str (O00O00O0000O0000O -1 )+O00O00OOO00O0O00O [6 :]#line:136
                OO000O0O0OOO0O0OO [OOOOOOO00O0O0O0O0 ]=OO000O0O0OOO0O0OO .pop (O00O00OOO00O0O00O )#line:137
        O0OO0OOOO000OO0O0 .load_state_dict (OO000O0O0OOO0O0OO ,strict =False )#line:140
    def add_layer (OOOO000O0O000O0O0 ,conv_channels =1024 ,downsample =2 ,depth =1 ,block =Bottleneck ):#line:142
        ""#line:143
        OOOO000O0O000O0O0 ._make_layer (block ,conv_channels //block .expansion ,blocks =depth ,stride =downsample )#line:144
class ResNetBackboneGN (ResNetBackbone ):#line:149
    def __init__ (O00O0OOOO00OO0O00 ,OOOOOOO0OOO0OOOO0 ,num_groups =32 ):#line:151
        super ().__init__ (OOOOOOO0OOO0OOOO0 ,norm_layer =lambda O0O0OO000000OOOO0 :nn .GroupNorm (num_groups ,O0O0OO000000OOOO0 ))#line:152
    def init_backbone (OO0O0O0O0000O0OOO ,OO00O00OO0000OO00 ):#line:154
        ""#line:155
        with open (OO00O00OO0000OO00 ,'rb')as O00O000O0O0000O00 :#line:156
            OO00OO0000O000O0O =pickle .load (O00O000O0O0000O00 ,encoding ='latin1')#line:157
            OO00OO0000O000O0O =OO00OO0000O000O0O ['blobs']#line:158
        O0OOOO0000OOOOO0O =list (OO0O0O0O0000O0OOO .state_dict ().keys ())#line:160
        OOO0OO0O00OO0O000 ={}#line:161
        OO00O000OO00000O0 =lambda OOO0O0O00OO000OOO :('gn_s'if OOO0O0O00OO000OOO =='weight'else 'gn_b')#line:163
        OOO000O0OOO00OO0O =lambda O00O0OOOOO0OOO0O0 :'res'+str (int (O00O0OOOOO0OOO0O0 )+2 )#line:164
        O0OOO0OO0OOO00OOO =lambda O00O0OOO0OOO0O0OO :'branch2'+('a','b','c')[int (O00O0OOO0OOO0O0OO [-1 :])-1 ]#line:165
        for O00000OOO0OOO0O0O in O0OOOO0000OOOOO0O :#line:168
            O00O0OO000OO0O0O0 =O00000OOO0OOO0O0O .split ('.')#line:169
            O000O0O0O00O0O0OO =''#line:170
            if (O00O0OO000OO0O0O0 [0 ]=='conv1'):#line:172
                O000O0O0O00O0O0OO ='conv1_w'#line:173
            elif (O00O0OO000OO0O0O0 [0 ]=='bn1'):#line:174
                O000O0O0O00O0O0OO ='conv1_'+OO00O000OO00000O0 (O00O0OO000OO0O0O0 [1 ])#line:175
            elif (O00O0OO000OO0O0O0 [0 ]=='layers'):#line:176
                if int (O00O0OO000OO0O0O0 [1 ])>=OO0O0O0O0000O0OOO .num_base_layers :continue #line:177
                O000O0O0O00O0O0OO =OOO000O0OOO00OO0O (O00O0OO000OO0O0O0 [1 ])#line:179
                O000O0O0O00O0O0OO +='_'+O00O0OO000OO0O0O0 [2 ]+'_'#line:180
                if O00O0OO000OO0O0O0 [3 ]=='downsample':#line:182
                    O000O0O0O00O0O0OO +='branch1_'#line:183
                    if O00O0OO000OO0O0O0 [4 ]=='0':#line:185
                        O000O0O0O00O0O0OO +='w'#line:186
                    else :#line:187
                        O000O0O0O00O0O0OO +=OO00O000OO00000O0 (O00O0OO000OO0O0O0 [5 ])#line:188
                else :#line:189
                    O000O0O0O00O0O0OO +=O0OOO0OO0OOO00OOO (O00O0OO000OO0O0O0 [3 ])+'_'#line:190
                    if 'conv'in O00O0OO000OO0O0O0 [3 ]:#line:192
                        O000O0O0O00O0O0OO +='w'#line:193
                    else :#line:194
                        O000O0O0O00O0O0OO +=OO00O000OO00000O0 (O00O0OO000OO0O0O0 [4 ])#line:195
            OOO0OO0O00OO0O000 [O00000OOO0OOO0O0O ]=torch .Tensor (OO00OO0000O000O0O [O000O0O0O00O0O0OO ])#line:197
        OO0O0O0O0000O0OOO .load_state_dict (OOO0OO0O00OO0O000 ,strict =False )#line:200
def darknetconvlayer (O00O00OOOOO00OOO0 ,OOOOO000O00OOO0O0 ,*O00000OO000OO0O00 ,**O0O00OO0OO0OO00OO ):#line:208
    ""#line:212
    return nn .Sequential (nn .Conv2d (O00O00OOOOO00OOO0 ,OOOOO000O00OOO0O0 ,*O00000OO000OO0O00 ,**O0O00OO0OO0OO00OO ,bias =False ),nn .BatchNorm2d (OOOOO000O00OOO0O0 ),nn .LeakyReLU (0.1 ,inplace =True ))#line:219
class DarkNetBlock (nn .Module ):#line:221
    ""#line:222
    expansion =2 #line:224
    def __init__ (O00OO00O0O0000O0O ,O00OO00O0000OOO0O ,OO0O00O0000O00OO0 ):#line:226
        super ().__init__ ()#line:227
        O00OO00O0O0000O0O .conv1 =darknetconvlayer (O00OO00O0000OOO0O ,OO0O00O0000O00OO0 ,kernel_size =1 )#line:229
        O00OO00O0O0000O0O .conv2 =darknetconvlayer (OO0O00O0000O00OO0 ,OO0O00O0000O00OO0 *O00OO00O0O0000O0O .expansion ,kernel_size =3 ,padding =1 )#line:230
    def forward (O00OOOO00000O0OO0 ,O0OOOOO0OO0OOO0O0 ):#line:232
        return O00OOOO00000O0OO0 .conv2 (O00OOOO00000O0OO0 .conv1 (O0OOOOO0OO0OOO0O0 ))+O0OOOOO0OO0OOO0O0 #line:233
class DarkNetBackbone (nn .Module ):#line:238
    ""#line:244
    def __init__ (O0OO0O0OOO0OO0OOO ,layers =[1 ,2 ,8 ,8 ,4 ],block =DarkNetBlock ):#line:246
        super ().__init__ ()#line:247
        O0OO0O0OOO0OO0OOO .num_base_layers =len (layers )#line:250
        O0OO0O0OOO0OO0OOO .layers =nn .ModuleList ()#line:251
        O0OO0O0OOO0OO0OOO .channels =[]#line:252
        O0OO0O0OOO0OO0OOO ._preconv =darknetconvlayer (3 ,32 ,kernel_size =3 ,padding =1 )#line:254
        O0OO0O0OOO0OO0OOO .in_channels =32 #line:255
        O0OO0O0OOO0OO0OOO ._make_layer (block ,32 ,layers [0 ])#line:257
        O0OO0O0OOO0OO0OOO ._make_layer (block ,64 ,layers [1 ])#line:258
        O0OO0O0OOO0OO0OOO ._make_layer (block ,128 ,layers [2 ])#line:259
        O0OO0O0OOO0OO0OOO ._make_layer (block ,256 ,layers [3 ])#line:260
        O0OO0O0OOO0OO0OOO ._make_layer (block ,512 ,layers [4 ])#line:261
        O0OO0O0OOO0OO0OOO .backbone_modules =[O0000O00O00000O00 for O0000O00O00000O00 in O0OO0O0OOO0OO0OOO .modules ()if isinstance (O0000O00O00000O00 ,nn .Conv2d )]#line:267
    def _make_layer (O0OO0OO0O0000O0O0 ,O00OOO00OOOO0OO0O ,OOOO0OO0000O00000 ,OO0O0O00OOO00O0O0 ,stride =2 ):#line:269
        ""#line:270
        O0O0O0000O00000O0 =[]#line:271
        O0O0O0000O00000O0 .append (darknetconvlayer (O0OO0OO0O0000O0O0 .in_channels ,OOOO0OO0000O00000 *O00OOO00OOOO0OO0O .expansion ,kernel_size =3 ,padding =1 ,stride =stride ))#line:276
        O0OO0OO0O0000O0O0 .in_channels =OOOO0OO0000O00000 *O00OOO00OOOO0OO0O .expansion #line:279
        O0O0O0000O00000O0 +=[O00OOO00OOOO0OO0O (O0OO0OO0O0000O0O0 .in_channels ,OOOO0OO0000O00000 )for _O0000OOO0OO00OOOO in range (OO0O0O00OOO00O0O0 )]#line:280
        O0OO0OO0O0000O0O0 .channels .append (O0OO0OO0O0000O0O0 .in_channels )#line:282
        O0OO0OO0O0000O0O0 .layers .append (nn .Sequential (*O0O0O0000O00000O0 ))#line:283
    def forward (O00OO0OOO0O0OOO00 ,O00OO00OO0OOOO0O0 ):#line:285
        ""#line:286
        O00OO00OO0OOOO0O0 =O00OO0OOO0O0OOO00 ._preconv (O00OO00OO0OOOO0O0 )#line:288
        O000OO0O0O0O000O0 =[]#line:290
        for OO0O00O0OO0OO0000 in O00OO0OOO0O0OOO00 .layers :#line:291
            O00OO00OO0OOOO0O0 =OO0O00O0OO0OO0000 (O00OO00OO0OOOO0O0 )#line:292
            O000OO0O0O0O000O0 .append (O00OO00OO0OOOO0O0 )#line:293
        return tuple (O000OO0O0O0O000O0 )#line:295
    def add_layer (O0OOOOO000OO0000O ,conv_channels =1024 ,stride =2 ,depth =1 ,block =DarkNetBlock ):#line:297
        ""#line:298
        O0OOOOO000OO0000O ._make_layer (block ,conv_channels //block .expansion ,num_blocks =depth ,stride =stride )#line:299
    def init_backbone (O00OOOOOO0OO000OO ,OOO00OO0O0000O0O0 ):#line:301
        ""#line:302
        O00OOOOOO0OO000OO .load_state_dict (torch .load (OOO00OO0O0000O0O0 ),strict =False )#line:304
class VGGBackbone (nn .Module ):#line:310
    ""#line:319
    def __init__ (O0O0O00OO00O000OO ,OOOOOO00OO0OOO000 ,extra_args =[],norm_layers =[]):#line:321
        super ().__init__ ()#line:322
        O0O0O00OO00O000OO .channels =[]#line:324
        O0O0O00OO00O000OO .layers =nn .ModuleList ()#line:325
        O0O0O00OO00O000OO .in_channels =3 #line:326
        O0O0O00OO00O000OO .extra_args =list (reversed (extra_args ))#line:327
        O0O0O00OO00O000OO .total_layer_count =0 #line:332
        O0O0O00OO00O000OO .state_dict_lookup ={}#line:333
        for OOOO0O0OO00O0O0O0 ,OO0O0000OO000OO0O in enumerate (OOOOOO00OO0OOO000 ):#line:335
            O0O0O00OO00O000OO ._make_layer (OO0O0000OO000OO0O )#line:336
        O0O0O00OO00O000OO .norms =nn .ModuleList ([nn .BatchNorm2d (O0O0O00OO00O000OO .channels [OOOOO0OO00O0O00OO ])for OOOOO0OO00O0O00OO in norm_layers ])#line:338
        O0O0O00OO00O000OO .norm_lookup ={OOOO00OO00OOO000O :OOO0OO000O0000000 for OOO0OO000O0000000 ,OOOO00OO00OOO000O in enumerate (norm_layers )}#line:339
        O0O0O00OO00O000OO .backbone_modules =[O00O0000000O00O00 for O00O0000000O00O00 in O0O0O00OO00O000OO .modules ()if isinstance (O00O0000000O00O00 ,nn .Conv2d )]#line:343
    def _make_layer (O0O0000OO0OOOO0OO ,O0O00O00O00000OOO ):#line:345
        ""#line:349
        OO0000OOO0OOO00O0 =[]#line:351
        for OO000O0OOO0OOOO00 in O0O00O00O00000OOO :#line:353
            O0O0OO00O0OO000O0 =None #line:356
            if isinstance (OO000O0OOO0OOOO00 ,tuple ):#line:357
                O0O0OO00O0OO000O0 =OO000O0OOO0OOOO00 [1 ]#line:358
                OO000O0OOO0OOOO00 =OO000O0OOO0OOOO00 [0 ]#line:359
            if OO000O0OOO0OOOO00 =='M':#line:362
                if O0O0OO00O0OO000O0 is None :#line:364
                    O0O0OO00O0OO000O0 ={'kernel_size':2 ,'stride':2 }#line:365
                OO0000OOO0OOO00O0 .append (nn .MaxPool2d (**O0O0OO00O0OO000O0 ))#line:367
            else :#line:368
                O00OO0O000O000O00 =O0O0000OO0OOOO0OO .total_layer_count +len (OO0000OOO0OOO00O0 )#line:370
                O0O0000OO0OOOO0OO .state_dict_lookup [O00OO0O000O000O00 ]='%d.%d'%(len (O0O0000OO0OOOO0OO .layers ),len (OO0000OOO0OOO00O0 ))#line:371
                if O0O0OO00O0OO000O0 is None :#line:374
                    O0O0OO00O0OO000O0 ={'kernel_size':3 ,'padding':1 }#line:375
                OO0000OOO0OOO00O0 .append (nn .Conv2d (O0O0000OO0OOOO0OO .in_channels ,OO000O0OOO0OOOO00 ,**O0O0OO00O0OO000O0 ))#line:378
                OO0000OOO0OOO00O0 .append (nn .ReLU (inplace =True ))#line:379
                O0O0000OO0OOOO0OO .in_channels =OO000O0OOO0OOOO00 #line:380
        O0O0000OO0OOOO0OO .total_layer_count +=len (OO0000OOO0OOO00O0 )#line:382
        O0O0000OO0OOOO0OO .channels .append (O0O0000OO0OOOO0OO .in_channels )#line:383
        O0O0000OO0OOOO0OO .layers .append (nn .Sequential (*OO0000OOO0OOO00O0 ))#line:384
    def forward (O0OO00OOO00O00O0O ,O0O00O0OO0O000000 ):#line:386
        ""#line:387
        OOOO00O000O0OO000 =[]#line:388
        for O0O0000O00000O000 ,O0O0OO0O0O00O0O00 in enumerate (O0OO00OOO00O00O0O .layers ):#line:390
            O0O00O0OO0O000000 =O0O0OO0O0O00O0O00 (O0O00O0OO0O000000 )#line:391
            if O0O0000O00000O000 in O0OO00OOO00O00O0O .norm_lookup :#line:395
                O0O00O0OO0O000000 =O0OO00OOO00O00O0O .norms [O0OO00OOO00O00O0O .norm_lookup [O0O0000O00000O000 ]](O0O00O0OO0O000000 )#line:396
            OOOO00O000O0OO000 .append (O0O00O0OO0O000000 )#line:397
        return tuple (OOOO00O000O0OO000 )#line:399
    def transform_key (OOO0OOO000O000O00 ,OOO0OOOO0000O0OOO ):#line:401
        ""#line:402
        O00000O00O0OO00O0 =OOO0OOOO0000O0OOO .split ('.')#line:403
        O000OOO000O0OO0O0 =OOO0OOO000O000O00 .state_dict_lookup [int (O00000O00O0OO00O0 [0 ])]#line:404
        return 'layers.%s.%s'%(O000OOO000O0OO0O0 ,O00000O00O0OO00O0 [1 ])#line:405
    def init_backbone (O0OOOO0OOOOOOOOOO ,O0OO0O0OO0O0OOO00 ):#line:407
        ""#line:408
        O000OO0OOO00O0000 =torch .load (O0OO0O0OO0O0OOO00 )#line:409
        O000OO0OOO00O0000 =OrderedDict ([(O0OOOO0OOOOOOOOOO .transform_key (O000OO000O0OO000O ),OOOO00000O0OOOOO0 )for O000OO000O0OO000O ,OOOO00000O0OOOOO0 in O000OO0OOO00O0000 .items ()])#line:410
        O0OOOO0OOOOOOOOOO .load_state_dict (O000OO0OOO00O0000 ,strict =False )#line:412
    def add_layer (O0OOOOOOOO0000O00 ,conv_channels =128 ,downsample =2 ):#line:414
        ""#line:415
        if len (O0OOOOOOOO0000O00 .extra_args )>0 :#line:416
            conv_channels ,downsample =O0OOOOOOOO0000O00 .extra_args .pop ()#line:417
        OOO0O0O0OO00000O0 =1 if downsample >1 else 0 #line:419
        O0O0OOOO0OOO000O0 =nn .Sequential (nn .Conv2d (O0OOOOOOOO0000O00 .in_channels ,conv_channels ,kernel_size =1 ),nn .ReLU (inplace =True ),nn .Conv2d (conv_channels ,conv_channels *2 ,kernel_size =3 ,stride =downsample ,padding =OOO0O0O0OO00000O0 ),nn .ReLU (inplace =True ))#line:426
        O0OOOOOOOO0000O00 .in_channels =conv_channels *2 #line:428
        O0OOOOOOOO0000O00 .channels .append (O0OOOOOOOO0000O00 .in_channels )#line:429
        O0OOOOOOOO0000O00 .layers .append (O0O0OOOO0OOO000O0 )#line:430
def construct_backbone (OO0OO0O0OO0O0O000 ):#line:435
    ""#line:436
    OOO0O0000000OOO0O =OO0OO0O0OO0O0O000 .type (*OO0OO0O0OO0O0O000 .args )#line:437
    O000O00OOOO0O00O0 =max (OO0OO0O0OO0O0O000 .selected_layers )+1 #line:440
    while len (OOO0O0000000OOO0O .layers )<O000O00OOOO0O00O0 :#line:442
        OOO0O0000000OOO0O .add_layer ()#line:443
    return OOO0O0000000OOO0O #line:445
