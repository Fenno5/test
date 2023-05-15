# coding=utf-8
# Copyright 2023 The Google Research Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

r"""Ground truth values for `german_credit_numeric_with_test_sparse_logistic_regression`."""

import numpy as np

PARAMS_MEAN: np.ndarray = np.array([
    -1.1838851267416666,
    1.0059914494179805,
    -1.0380936008221013,
    0.42841185011358596,
    -0.9674014534941406,
    -0.6549982166162993,
    -0.2107040125304899,
    -0.07739429755818186,
    0.7565319305257808,
    -0.28419896987171034,
    -0.742617803871896,
    0.46553108544053223,
    -0.0015668160573959259,
    -0.6223828083288044,
    -0.8336673737094527,
    0.7953585919647085,
    -0.8658881317229088,
    0.6010881604881895,
    0.7516534603918409,
    0.21155297753118213,
    -0.36974589585691925,
    -0.10978624983135435,
    -0.0007779317310475013,
    0.0355824067624817,
    -1.3336557175080002,
    2.4439010026026664,
    1.674765021480318,
    1.7932340821347843,
    0.6136909648053737,
    1.51467537955159,
    0.8161300923770367,
    0.3904371941611651,
    0.36680198109322104,
    1.0088795651500453,
    0.4515115026180969,
    0.9280353201286664,
    0.6029283115574513,
    0.3468666388809409,
    0.7783922276226264,
    1.182414764875162,
    1.0399347275051336,
    1.241251855731462,
    0.8263362337619607,
    1.0223875563837959,
    0.44737122679785035,
    0.5440297031154755,
    0.3647276043157606,
    0.37259531531480305,
    0.36676433072893144,
    3.2286390193640004,
    0.36594427819919995,
]).reshape((51,))

PARAMS_MEAN_STANDARD_ERROR: np.ndarray = np.array([
    0.0005981660464235878,
    0.0006135876540999674,
    0.0006132548865209968,
    0.000803377297419766,
    0.0006049782223892016,
    0.000771292967698475,
    0.0007774783903198308,
    0.0007659490351722464,
    0.0008049962237919129,
    0.0007893216669665765,
    0.0007721116046629342,
    0.0008030001846045975,
    0.0007530940897997456,
    0.0007837046272220854,
    0.0007537488478658359,
    0.0007551929529850969,
    0.0007275810106867986,
    0.0009107156036158675,
    0.0008380421358340607,
    0.0008027590248072173,
    0.000846842591322889,
    0.0007770780743274671,
    0.0007431850802852932,
    0.000757876544618884,
    0.0006592016543744323,
    0.0016674727697632262,
    0.0013373333345408193,
    0.0014172343648693945,
    0.0009208409611009669,
    0.0012925597320408856,
    0.0010240743950809543,
    0.000665833848910506,
    0.0005727478123486804,
    0.0011809240640211491,
    0.0006774109626239607,
    0.0011085220063862288,
    0.0008927776683871067,
    0.0005607264239990413,
    0.0010691700039338601,
    0.0012393408295048253,
    0.0012373207240113956,
    0.0012589868491428302,
    0.001250630244548729,
    0.0012793885048060923,
    0.0006897384909408552,
    0.0007810885576205727,
    0.0005958773232696626,
    0.0005699488539133139,
    0.0005909674993432928,
    0.0022468031264735837,
    0.0002711192882221147,
]).reshape((51,))

PARAMS_STANDARD_DEVIATION: np.ndarray = np.array([
    0.5692117195860952,
    0.5677421529175252,
    0.562277138614212,
    0.7892247581272893,
    0.5660226933295356,
    0.691689221495052,
    0.8071941992835272,
    0.823920491277778,
    0.6567992672766995,
    0.8035247310142861,
    0.6409207318443784,
    0.7669103963270938,
    0.8209748967688372,
    0.7079062958936378,
    0.6293368138798237,
    0.6233261155952887,
    0.6068794880781312,
    0.7424100127193938,
    0.6681241435870447,
    0.8244839092591019,
    0.7982633705938547,
    0.8186456335220941,
    0.8280317028703763,
    0.8250445765335408,
    0.5765291148513438,
    1.5065700228426764,
    1.2708158068948712,
    1.2953232321587766,
    0.8677959268703033,
    1.209475774208417,
    0.959992910035797,
    0.6680939493819217,
    0.6426845158867424,
    1.0589135045514155,
    0.7245789915824581,
    0.993230463704737,
    0.8432012939457578,
    0.6203093523335816,
    0.943026246915948,
    1.1330109879905408,
    1.0468797941904935,
    1.14060323931888,
    1.0014950042286426,
    1.0722476046007519,
    0.7213365756284413,
    0.8029465429365654,
    0.6419600178748756,
    0.6487860091686608,
    0.6424489834913355,
    1.7568431706964294,
    0.1579495547414705,
]).reshape((51,))

PER_EXAMPLE_TEST_NLL_MEAN: np.ndarray = np.array([
    0.8932802985806665,
    0.8805982137320001,
    0.07281155224717999,
    0.9696056991333333,
    1.6555208475533334,
    0.23406506287579995,
    0.11815078074993335,
    0.04570794983766,
    0.6878347782614667,
    0.4600854188124,
    0.929148332632,
    0.11039605532619998,
    0.5900256371900001,
    0.05600385689016,
    0.11208472671766664,
    0.2830690590789334,
    0.040564828436726,
    1.0367364725576667,
    0.26402510842353333,
    0.13792483890593332,
    0.722906202488,
    0.11671178047146669,
    0.9805809884439334,
    1.6982768760573337,
    0.6280893774479999,
    0.1121140445752,
    1.0448789837586667,
    0.49211185157,
    0.21612400629286665,
    0.5936031824406667,
    1.1891306144279998,
    0.21368964659513331,
    0.10598263353479997,
    0.35968327909579995,
    0.05922757560342,
    0.21453071531793336,
    0.8167858978053333,
    0.9226470367146667,
    1.6739274616213333,
    0.2059964318222,
    0.061943855831933334,
    1.4196761859882667,
    0.27310091894846666,
    1.9685428938179999,
    0.7486841133025333,
    0.32431026917820005,
    0.15231322856,
    0.2810245611262667,
    0.2262218080458,
    0.2320797038295333,
    0.24237465992033336,
    0.147699391710502,
    0.03580297003770001,
    0.04784709383689333,
    2.257388003131333,
    0.2823087150972,
    0.15069805655253332,
    0.4023085103093334,
    0.24900819939513336,
    0.03616694009950334,
    0.2061633290075333,
    0.11161810852027332,
    1.1207777654920001,
    1.545352750278,
    0.18583755919926664,
    0.8644224076466667,
    0.18665400533333334,
    0.15555939496553334,
    0.13014888101053335,
    0.03664557280752666,
    0.6494967742393334,
    0.2941871563751334,
    0.2889536361571333,
    0.24962913162800002,
    0.49207019825173326,
    1.1510740997213333,
    0.8329377725120001,
    0.19200160236973335,
    0.14537038947793332,
    0.11181803228066664,
    0.3127595554272,
    0.03239767553237133,
    0.30491776777580004,
    0.8088852840606666,
    0.7558027646053334,
    0.057796918749126666,
    0.5764735361079999,
    0.2501331716055334,
    1.7948774935226666,
    0.6947927857393333,
    0.8983110609686668,
    1.567359699042,
    1.4142068950033333,
    0.730860043442,
    1.7710474526253335,
    0.6017339474286667,
    0.749811021938,
    0.1118560518586,
    0.5682557513679999,
    0.38729974644399995,
    0.2816426459196,
    0.05467074141433333,
    0.7718351100593333,
    0.1667896605224,
    0.3119883308179999,
    0.13536394779188668,
    0.9178761668906663,
    0.44131320456519996,
    0.06658872596986667,
    1.2863488526326665,
    0.04631893589452667,
    0.19453692593639998,
    0.5028246541526668,
    0.028845926386493324,
    0.46592164511173334,
    0.5076860763915334,
    0.8270957236898001,
    0.07363693203990666,
    1.4723151542153332,
    0.12480194739273334,
    1.4880357725780666,
    0.01962631420628133,
    0.5645879731626666,
    0.06788400987932666,
    0.7549323627757332,
    0.12088377891893336,
    0.3967343325802667,
    0.3011679270792667,
    1.8095277259,
    0.23377042774520002,
    0.09137190347906665,
    0.6514547235018666,
    1.5451398924420001,
    1.2845736072493998,
    0.4688204046366667,
    0.46958583356479994,
    0.13690902913453334,
    0.60335870604,
    0.3253230410302,
    0.625201563154,
    1.9678167017879997,
    0.027051042997486667,
    0.34268634162173334,
    0.2876715895887333,
    0.19654652381566667,
    0.3368272875571333,
    0.20043682701610868,
    0.02639687867358,
    0.07038683047575334,
    1.0039479645593332,
    0.11704837096753336,
    0.038846639525936,
    1.2944749141606668,
    0.200117590195,
    0.5280947220835334,
    0.10819592967340667,
    0.08957297113539332,
    0.19915713105326666,
    0.2508756714848,
    0.6654825840224666,
    0.18839285406499998,
    0.26009153379333333,
    0.7107080698952,
    0.06831037274867333,
    0.22442168287003997,
    0.16220565458480002,
    0.3574284081358,
    0.27277224430086666,
    2.1643369750226666,
    1.5271146576286667,
    3.39686751388,
    0.09534177339573333,
    0.7024778671526667,
    0.2742506722181334,
    0.1242365225118,
    0.29555073333079995,
    1.1505656520653331,
    0.1303518809298933,
    0.5711314973851334,
    0.5650289145466668,
    0.7564385054113333,
    0.04193295254096667,
    0.5362276295793333,
    0.12413039833002666,
    0.596463325482,
    2.6180225795533336,
    1.300850718916,
    0.125580339638,
    2.1985649611913334,
    0.11614611674899997,
    0.4298701917603333,
    0.1617380555714,
    0.8716859400560001,
    0.5417966828789333,
    1.0740642201193336,
    0.09689275426793334,
    0.8125607004706668,
    0.18467196175659334,
    0.06233246876997334,
    0.055702146692313326,
    0.23313085222080004,
    1.0521178133963331,
    0.27470644321119997,
    0.6188661788486667,
    0.04665166994681666,
    0.6237205510606667,
    0.3962529994002667,
    0.696233716036,
    0.10006141391909332,
    0.15355236612273332,
    0.2295005324601333,
    1.9570544718693335,
    0.5270949862324666,
    2.15984109137,
    1.3971375662206666,
    0.060433736697293336,
    0.951622933616,
    0.5389614065448,
    0.2442092646370667,
    0.2953145316329334,
    0.38661033270833334,
    0.22969068909986662,
    0.7347364076233334,
    0.28590243673646665,
    0.5616320499584,
    0.16576861787206665,
    0.18062649420206664,
    0.22918376737266666,
    0.3864906409583333,
    0.23430458785193334,
    0.15875909530953333,
    0.6971458376559333,
    0.09057607382153332,
    0.08572732540012667,
    0.5429912861110667,
    1.3043550583725334,
    0.20225930718653334,
    1.1258259671913335,
    0.47547891463806663,
    0.4234302535124,
    0.18131325537266665,
    0.1891564493292,
    0.14857409147016,
    0.1719800655262,
    0.05115110293182,
    0.23237854730566668,
    0.15236638079620002,
    0.02799980400684,
    1.254673685934667,
    0.040121037181924,
]).reshape((250,))

PER_EXAMPLE_TEST_NLL_MEAN_STANDARD_ERROR: np.ndarray = np.array([
    0.00032153712196378206,
    0.00023987491920897367,
    2.9056972772856642e-05,
    0.00021166578233862928,
    0.00043286735427594677,
    9.474655265972705e-05,
    3.6769971555736415e-05,
    2.22790724281724e-05,
    0.00034757760926201157,
    0.0001459733449800984,
    0.00027568474103784854,
    3.9717712692023445e-05,
    0.00017102139654367904,
    2.8998965590756203e-05,
    3.534369220060247e-05,
    0.00010969792072407062,
    4.9465862687622044e-05,
    0.000497900287430413,
    0.00012016042562926001,
    3.556406055866058e-05,
    0.0002100447023359982,
    3.369774407451265e-05,
    0.00041235201732991945,
    0.00045150835143756247,
    0.00015957255930384458,
    4.291421452093546e-05,
    0.00031217327310758576,
    0.0001340016008333503,
    8.040957621534812e-05,
    0.00018643402374624683,
    0.00026816261372477376,
    9.136803189307127e-05,
    4.700313966486291e-05,
    0.00012949625147407127,
    2.8826699808503546e-05,
    0.00013252988171583857,
    0.00025625911646822076,
    0.0002850216055911534,
    0.00041410518418894617,
    9.184207067944421e-05,
    3.03933388399952e-05,
    0.0005554639477388119,
    0.00016596127561907965,
    0.0006557803120425634,
    0.0002654605779504038,
    0.00015384544699978154,
    7.419344722973179e-05,
    6.998155213847191e-05,
    0.00010415274709450757,
    0.00010972086803592591,
    0.00018098690159083975,
    0.0001578116214151066,
    2.0750929712384972e-05,
    2.1151313324986292e-05,
    0.00042567280979356476,
    0.0001081758655083595,
    4.916957476257293e-05,
    0.00013003969123315395,
    8.584358742796228e-05,
    4.975657824560633e-05,
    9.530194046452203e-05,
    8.151421958960496e-05,
    0.0002288372526354027,
    0.0002384287219728366,
    0.00010953419199016353,
    0.00032105858409531746,
    8.742810825880636e-05,
    5.039293622766902e-05,
    5.390853654712829e-05,
    2.3442820198379243e-05,
    0.00012335258128747694,
    0.0001523505347439892,
    0.0001759768093202779,
    0.00010161254101374626,
    0.00022097449441655658,
    0.00020583926408299132,
    0.00015585091573371853,
    7.693969182352437e-05,
    4.6398276418383935e-05,
    5.314551551227712e-05,
    0.00012298472668576045,
    2.2133134265128136e-05,
    0.00011886588280429521,
    0.00015598073357127003,
    0.00017081863058799953,
    3.064514213766753e-05,
    0.00020484644532236276,
    7.584550162732319e-05,
    0.0003990340395200468,
    0.0002052111534213109,
    0.0002778123409407707,
    0.0003901784836145747,
    0.0003551264268598599,
    0.00023809726726717093,
    0.00039583365414470705,
    0.000175770043894884,
    0.0002469729935741937,
    3.4068457267907234e-05,
    0.0001857752537767532,
    0.00023276911935070368,
    9.676012056608388e-05,
    2.4574360954064275e-05,
    0.00024108618293458304,
    5.360904767100146e-05,
    0.00011168609490095625,
    8.839929397645976e-05,
    0.0003252014286279444,
    0.0003469966836000381,
    2.062502993905412e-05,
    0.0004844893081670843,
    2.3621884246583598e-05,
    0.00010410044486011985,
    0.00011066478748694188,
    1.9195262126370067e-05,
    0.00017961628230170025,
    0.00021736222737213,
    0.0004032331462548495,
    4.290553529876965e-05,
    0.000408269282913353,
    5.240574151915042e-05,
    0.0007801616684809686,
    1.3000696714067651e-05,
    0.0001769712836205073,
    3.948675865930506e-05,
    0.0002924712429698084,
    4.994857839539926e-05,
    0.00017969868888541312,
    9.443455997663064e-05,
    0.0003629153109308881,
    0.00010333089822221198,
    3.9827197498076646e-05,
    0.00025940704021357625,
    0.00032417917681847253,
    0.0005493148184189602,
    0.0001224682108357506,
    0.0001450591539849271,
    5.033920443961946e-05,
    0.00018814297962652638,
    0.00011490494407704568,
    0.00023046371713432656,
    0.0003918038855148469,
    1.3416454041465919e-05,
    0.00011616689700913684,
    8.678529436974346e-05,
    6.0908987028661074e-05,
    7.572097416087637e-05,
    0.00023830793709131456,
    1.1944204971171449e-05,
    4.3503911130069016e-05,
    0.00017726403868561054,
    3.579977892831471e-05,
    3.4551969721394e-05,
    0.0003460133138490385,
    4.8068410377227915e-05,
    0.00023373050862508218,
    5.4372061147928335e-05,
    9.144495759228718e-05,
    0.00010997006691395534,
    7.909131135256938e-05,
    0.0002700860243563609,
    0.00011594640500683878,
    0.00011044213886367434,
    0.0003295419703947446,
    2.9710761417678753e-05,
    0.0001466843454372131,
    6.741972049143248e-05,
    0.0001128600791970681,
    8.472937726513761e-05,
    0.0007336297460907198,
    0.000544958686805171,
    0.0005650413777817236,
    2.6236226766601777e-05,
    0.0001412604475692239,
    0.00011517438650125967,
    4.127009696264485e-05,
    0.00011654236679867573,
    0.0006248258703969294,
    9.077588227080383e-05,
    0.000304977940964981,
    0.0002477401379619092,
    0.0002285837385799114,
    1.8422580299896414e-05,
    0.0001529871110784206,
    7.210337453730762e-05,
    0.00017938448740229278,
    0.0006070594823202606,
    0.00037804892480219947,
    4.3479931953811176e-05,
    0.00047759954736740476,
    4.0973389923993534e-05,
    0.00015223423059360924,
    6.814082902388355e-05,
    0.00020674150810314311,
    0.0001852605573179122,
    0.00025594312192626033,
    3.814489428680866e-05,
    0.00031417815278787624,
    0.00012189063454042425,
    2.3606224017910556e-05,
    3.468171843799626e-05,
    0.0001230462495298638,
    0.0003943005087404004,
    9.28050680822266e-05,
    0.00016763756824874365,
    6.257037365733747e-05,
    0.00022115186920846147,
    0.00015781584715620332,
    0.00012721766852535148,
    4.8587934947068584e-05,
    6.606508615603971e-05,
    9.318169782027268e-05,
    0.00036506615387339644,
    0.00018105688558136954,
    0.00040738379428702215,
    0.00026417956174610224,
    2.5832121679318452e-05,
    0.0002525800553239043,
    0.00022304003698103006,
    0.00011417532664578275,
    0.00013378995878979302,
    0.00016986083408308326,
    9.107894958869919e-05,
    0.00016782775124419373,
    0.00010888453166183272,
    0.00022322614261667225,
    8.120066736622856e-05,
    8.17154685210108e-05,
    0.00022439578193871545,
    0.0002324824393590016,
    0.00015101111591184555,
    4.9074503238359104e-05,
    0.00040182055800629004,
    3.066480963829134e-05,
    5.632657901197814e-05,
    0.00021451828428282717,
    0.000597946126757927,
    7.668893390682197e-05,
    0.00023854946620907374,
    0.00020898795823861847,
    0.00013923696647332034,
    5.0201128326308424e-05,
    8.396976091974454e-05,
    0.00010108566712236049,
    4.77951740702592e-05,
    2.7079409244519088e-05,
    7.186940369354517e-05,
    6.054115596412238e-05,
    2.0033849466202603e-05,
    0.0003309812625048176,
    5.486107033374318e-05,
]).reshape((250,))

PER_EXAMPLE_TEST_NLL_STANDARD_DEVIATION: np.ndarray = np.array([
    0.26870590581007175,
    0.2217099414120239,
    0.028994763913104814,
    0.1999899644680198,
    0.3486194966246353,
    0.0882674294673305,
    0.035806440122558826,
    0.019782012312970602,
    0.2732964334600797,
    0.12866777854504527,
    0.24723123198875507,
    0.041463456203576,
    0.15440953761741166,
    0.025449356696734517,
    0.034439140897084435,
    0.09568109419435025,
    0.03228638118348737,
    0.35493375591640897,
    0.1090449013422922,
    0.0331399801182846,
    0.17481850313469502,
    0.033505632228384555,
    0.3506596768938177,
    0.3377623166327418,
    0.15027609441319847,
    0.03688291973145708,
    0.27472770386128964,
    0.11535162069644271,
    0.07188915885513883,
    0.1686171722435377,
    0.23594136851152725,
    0.07516589740138449,
    0.04112877709986131,
    0.11747513623886345,
    0.02511997886408359,
    0.12140725090542837,
    0.21932672290437974,
    0.25251746560936983,
    0.3216304432907333,
    0.08404016877963255,
    0.027289303460650775,
    0.535515639181839,
    0.11159969658621757,
    0.5405717749540634,
    0.2414805556820765,
    0.12175910203198075,
    0.06643262574499945,
    0.06524762991037394,
    0.09590604257529335,
    0.09429595046207012,
    0.1370962910819887,
    0.10705263571600035,
    0.017968146290713034,
    0.01858973640086307,
    0.3842366559941347,
    0.09806633942876164,
    0.05044543429564461,
    0.11419149056518363,
    0.08334854276850098,
    0.030221760976944068,
    0.08618651095243166,
    0.0595762654316076,
    0.20194423951961055,
    0.24208162475303469,
    0.09099225574121131,
    0.2529255976015715,
    0.0709658932540574,
    0.05173611684280135,
    0.04410837802766944,
    0.01891668973541581,
    0.1212535657741028,
    0.1470547242195373,
    0.12236960123323515,
    0.0852063318377774,
    0.1857070663477703,
    0.1767921623226157,
    0.1418863499876215,
    0.06823285600225194,
    0.04660994800992922,
    0.04242989951961966,
    0.1048066515085139,
    0.017025869574626006,
    0.09986619247806754,
    0.15582010911993338,
    0.16103410254059386,
    0.024981096320957873,
    0.17457996452373445,
    0.07450800259037783,
    0.3363511543192469,
    0.16283688404583618,
    0.21723566535385436,
    0.35484835035475865,
    0.29290743148381077,
    0.2103343106088003,
    0.34103254397135807,
    0.1498201003933424,
    0.22158985455393937,
    0.032715121609988906,
    0.1514649345744654,
    0.18592524953898643,
    0.09209051453181301,
    0.022870626159565578,
    0.20515713341635747,
    0.05184542906546079,
    0.09861245662163572,
    0.06539251351574366,
    0.29488988060939747,
    0.23889518197867815,
    0.020453018375294556,
    0.3932176084063769,
    0.019882295343682306,
    0.0976949509966712,
    0.10787145704382368,
    0.016009909734227064,
    0.15101422072258966,
    0.17379105603704603,
    0.274322218904628,
    0.03657354188965388,
    0.3350592088787028,
    0.044291069054555945,
    0.6572681233124966,
    0.010627006744534219,
    0.16112830431509956,
    0.03128091864501645,
    0.27903396882623577,
    0.04338389564722415,
    0.15860918464805612,
    0.08544691416417534,
    0.3070331829855171,
    0.09395302698072064,
    0.03592085410987787,
    0.22288929932687246,
    0.30818302277207194,
    0.4164513877514838,
    0.11515218877628915,
    0.13629912010979156,
    0.04138763303783175,
    0.1622715987615615,
    0.09898923505587526,
    0.19529996262513385,
    0.360578775645853,
    0.012002038711402319,
    0.09054402586263995,
    0.0845145451699156,
    0.05617260274414722,
    0.07179360123488963,
    0.15020935895248905,
    0.011088884595306908,
    0.03322367607762828,
    0.16135880197974697,
    0.03420337477427561,
    0.023891949710504363,
    0.28182998981590146,
    0.05031576483060035,
    0.20965439723235607,
    0.04860488081184116,
    0.06964023965267858,
    0.08809483159464274,
    0.07403454057109365,
    0.2288814286120875,
    0.10154106758703926,
    0.10057474819084714,
    0.32266699275810556,
    0.027446473561892597,
    0.09962166190881608,
    0.058195843212894616,
    0.10919409384773555,
    0.07542358601626517,
    0.6204737800635651,
    0.46789373027072073,
    0.4895211627903162,
    0.02675587932238126,
    0.12949666498288093,
    0.10028249755305937,
    0.03595281205921115,
    0.10850017647207592,
    0.44771603671335913,
    0.07916454904961388,
    0.262412763946681,
    0.1904060700247172,
    0.18859680317143404,
    0.015798223449583235,
    0.13310467279868995,
    0.061668809425952945,
    0.14916093397708888,
    0.5332644900134329,
    0.3246135500062896,
    0.0399701338038215,
    0.3864178405040727,
    0.03766581823967911,
    0.1402896874819159,
    0.05823300248888654,
    0.1939218158250446,
    0.1651622843555703,
    0.22700036941296883,
    0.033475707164925976,
    0.26124785735974376,
    0.08500662266629593,
    0.022315758852807496,
    0.030563817640353312,
    0.09903661281843554,
    0.3740792631036485,
    0.07651404131019925,
    0.15913123239034582,
    0.0422504320638421,
    0.1764359381351995,
    0.13499747955947156,
    0.13360075866437296,
    0.04416903629767875,
    0.057756627190915136,
    0.08187299041338668,
    0.3147691284101902,
    0.1600162423680936,
    0.3589557338592094,
    0.24172633110227984,
    0.023036657474523194,
    0.2353486037790884,
    0.18239232150673318,
    0.09429001991135842,
    0.10281453124009195,
    0.13415168173493047,
    0.07406423617878902,
    0.16603692213954888,
    0.09304832878807569,
    0.2017087450397049,
    0.06763377267666501,
    0.07215818427800608,
    0.15753018382355996,
    0.2161197246962323,
    0.1406374931676345,
    0.04988528973046572,
    0.2938798989221163,
    0.029855304358490837,
    0.0417605777397679,
    0.191639232903419,
    0.5407719433901764,
    0.06716596659602878,
    0.20782344642986664,
    0.18486552924330144,
    0.11970451222145784,
    0.054787703291929536,
    0.07470159174648763,
    0.06990358142403602,
    0.04649309164118321,
    0.024435158132194035,
    0.06619042731876243,
    0.05140282178085058,
    0.015066065924307795,
    0.3015167642555913,
    0.03288881522272262,
]).reshape((250,))

TEST_NLL_MEAN: np.ndarray = np.array([
    132.86829305266664,
]).reshape(())

TEST_NLL_MEAN_STANDARD_ERROR: np.ndarray = np.array([
    0.00315842068751233,
]).reshape(())

TEST_NLL_STANDARD_DEVIATION: np.ndarray = np.array([
    2.9687648183742548,
]).reshape(())
