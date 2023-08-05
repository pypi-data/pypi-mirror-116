#pragma once
/*
Copyright (C) 2017 Ming-Shing Chen

This file is part of BitPolyMul.

BitPolyMul is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

BitPolyMul is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with BitPolyMul.  If not, see <http://www.gnu.org/licenses/>.
*/


#include "libOTe/config.h"
#ifdef ENABLE_SILENTOT


#include "stdint.h"


namespace bpm {



    alignas(32) const uint64_t i_beta_mul_32_bm4r[(64 / 4) * 16 * 2] = {
    0x100c7c6c7c60100,0x405c2c3c2c30405, 0x100c7c6c7c60100,0x405c2c3c2c30405,
    0x9d6863960bfef500,0xfb0e05f06d989366, 0x9d6863960bfef500,0xfb0e05f06d989366,
    0xe1e15e5ebfbf0000,0xa0a01f1ffefe4141, 0xe1e15e5ebfbf0000,0xa0a01f1ffefe4141,
    0x44ae6288cc26ea00,0x45af6389cd27eb01, 0x44ae6288cc26ea00,0x45af6389cd27eb01,
    0xa5a5e4e441410000,0xe5e5a4a401014040, 0xa5a5e4e441410000,0xe5e5a4a401014040,
    0x1a1598978d820f00,0xa5aa2728323db0bf, 0x1a1598978d820f00,0xa5aa2728323db0bf,
    0x7e7e060678780000,0xaeaed6d6a8a8d0d0, 0x7e7e060678780000,0xaeaed6d6a8a8d0d0,
    0xd44337a074e39700,0x6afd891eca5d29be, 0xd44337a074e39700,0x6afd891eca5d29be,
    0xe9e963638a8a0000,0x80800a0ae3e36969, 0xe9e963638a8a0000,0x80800a0ae3e36969,
    0xc46115b571d4a00,0x2f653278743e6923, 0xc46115b571d4a00,0x2f653278743e6923,
    0xc7c7dcdc1b1b0000,0xe3e3f8f83f3f2424, 0xc7c7dcdc1b1b0000,0xe3e3f8f83f3f2424,
    0xf41f678c7893eb00,0x4ca7df34c02b53b8, 0xf41f678c7893eb00,0x4ca7df34c02b53b8,
    0xc0c0565696960000,0xf3f36565a5a53333, 0xc0c0565696960000,0xf3f36565a5a53333,
    0x3b2bafbf84941000,0xd9c94d5d6676f2e2, 0x3b2bafbf84941000,0xd9c94d5d6676f2e2,
    0xf5f5fdfd08080000,0x82828a8a7f7f7777, 0xf5f5fdfd08080000,0x82828a8a7f7f7777,
    0x1fce83524d9cd100,0xa3723feef1206dbc, 0x1fce83524d9cd100,0xa3723feef1206dbc,
    0x4e0f9edf91d04100,0xe6a736773978e9a8, 0x4e0f9edf91d04100,0xe6a736773978e9a8,
    0x8f69e606896fe00,0x946a02fcf40a629c, 0x8f69e606896fe00,0x946a02fcf40a629c,
    0x7bf5e36d16988e00,0x1d93850b70fee866, 0x7bf5e36d16988e00,0x1d93850b70fee866,
    0x42a1ad4e0cefe300,0x7e4e80b49aaa645, 0x42a1ad4e0cefe300,0x7e4e80b49aaa645,
    0xea6b5cdd37b68100,0x1998af2ec44572f3, 0xea6b5cdd37b68100,0x1998af2ec44572f3,
    0x1caa8f392593b600,0x3482a7110dbb9e28, 0x1caa8f392593b600,0x3482a7110dbb9e28,
    0xc39ef6ab68355d00,0x421f772ae9b4dc81, 0xc39ef6ab68355d00,0x421f772ae9b4dc81,
    0x2af3b069439ad900,0x29f0b36a4099da03, 0x2af3b069439ad900,0x29f0b36a4099da03,
    0x3853f19aa2c96b00,0x3c57f59ea6cd6f04, 0x3853f19aa2c96b00,0x3c57f59ea6cd6f04,
    0x8cf85e2aa6d27400,0xf5812753dfab0d79, 0x8cf85e2aa6d27400,0xf5812753dfab0d79,
    0x9ca9083da1943500,0xb3e9faa3603a297, 0x9ca9083da1943500,0xb3e9faa3603a297,
    0xadddc9b914647000,0xa9d9cdbd10607404, 0xadddc9b914647000,0xa9d9cdbd10607404,
    0x3fcc44b7887bf300,0x4ab931c2fd0e8675, 0x3fcc44b7887bf300,0x4ab931c2fd0e8675,
    0x3e01e5dae4db3f00,0xbe81655a645bbf80, 0x3e01e5dae4db3f00,0xbe81655a645bbf80,
    0xd8a2c6bc641e7a00,0x87fd99e33b41255f, 0xd8a2c6bc641e7a00,0x87fd99e33b41255f,
    0xc073ea59992ab300,0xfc4fd665a5168f3c, 0xc073ea59992ab300,0xfc4fd665a5168f3c,
    0x4346484d0e0b0500,0xfafff1f4b7b2bcb9, 0x4346484d0e0b0500,0xfafff1f4b7b2bcb9,
    0x40b6e11757a1f600,0x7c8add2b6b9dca3c, 0x40b6e11757a1f600,0x7c8add2b6b9dca3c,
    0x7a47764b310c3d00,0x320f3e0379447548, 0x7a47764b310c3d00,0x320f3e0379447548,
    0xba3c8b0db7318600,0x29af189e24a21593, 0xba3c8b0db7318600,0x29af189e24a21593,
    0x41eb1fb5f45eaa00,0xcb61953f7ed4208a, 0x41eb1fb5f45eaa00,0xcb61953f7ed4208a,
    0x1a73335a40296900,0x771e5e372d44046d, 0x1a73335a40296900,0x771e5e372d44046d,
    0xcc01a16ca06dcd00,0xf23f9f529e53f33e, 0xcc01a16ca06dcd00,0xf23f9f529e53f33e,
    0xa3b74753f0e41400,0xe3f70713b0a45440, 0xa3b74753f0e41400,0xe3f70713b0a45440,
    0x94954342d6d70100,0x6d6cbabb2f2ef8f9, 0x94954342d6d70100,0x6d6cbabb2f2ef8f9,
    0x51fa0aa1f05bab00,0xcb60903b6ac1319a, 0x51fa0aa1f05bab00,0xcb60903b6ac1319a,
    0x5252dddd8f8f0000,0xfafa75752727a8a8, 0x5252dddd8f8f0000,0xfafa75752727a8a8,
    0x1b418ed4cf955a00,0x540ec19b80da154f, 0x1b418ed4cf955a00,0x540ec19b80da154f,
    0xb27901ca78b3cb00,0xf03b43883af18942, 0xb27901ca78b3cb00,0xf03b43883af18942,
    0x13a143f1e250b200,0x45f715a7b406e456, 0x13a143f1e250b200,0x45f715a7b406e456,
    0x9d3006ab369bad00,0x6dc0f65bc66b5df0, 0x9d3006ab369bad00,0x6dc0f65bc66b5df0,
    0x3b7cdc9ba0e74700,0xaaed4d0a3176d691, 0x3b7cdc9ba0e74700,0xaaed4d0a3176d691,
    0x61cb3c96f75daa00,0x1ab047ed8c26d17b, 0x61cb3c96f75daa00,0x1ab047ed8c26d17b,
    0x60ad0bc6a66bcd00,0x9459ff32529f39f4, 0x60ad0bc6a66bcd00,0x9459ff32529f39f4,
    0x8db76953dee43a00,0x271dc3f9744e90aa, 0x8db76953dee43a00,0x271dc3f9744e90aa,
    0x7d17f09ae78d6a00,0x16b8ce69bf1167c, 0x7d17f09ae78d6a00,0x16b8ce69bf1167c,
    0x4192c5165784d300,0x1ac99e4d0cdf885b, 0x4192c5165784d300,0x1ac99e4d0cdf885b,
    0x50c2bc2e7eec9200,0x92ec7e2ebcc250, 0x50c2bc2e7eec9200,0x92ec7e2ebcc250,
    0x3f7da1e3dc9e4200,0x3072aeecd3914d0f, 0x3f7da1e3dc9e4200,0x3072aeecd3914d0f,
    0x2be3834b60a8c800,0x25ed8d456ea6c60e, 0x2be3834b60a8c800,0x25ed8d456ea6c60e,
    0xeea52b608ec54b00,0x4e058bc02e65eba0, 0xeea52b608ec54b00,0x4e058bc02e65eba0,
    0xa8f3aef55d065b00,0x89d28fd47c277a21, 0xa8f3aef55d065b00,0x89d28fd47c277a21,
    0x91b4a38617322500,0x80a5b29706233411, 0x91b4a38617322500,0x80a5b29706233411,
    0x91f897fe6f066900,0xec85ea83127b147d, 0x91f897fe6f066900,0xec85ea83127b147d,
    0xcd1ed201cc1fd300,0x34e72bf835e62af9, 0xcd1ed201cc1fd300,0x34e72bf835e62af9,
    0xf5ad346c99c15800,0xf5ad346c99c15800, 0xf5ad346c99c15800,0xf5ad346c99c15800,
    0x994724fa63bdde00,0x3be58658c11f7ca2, 0x994724fa63bdde00,0x3be58658c11f7ca2,
    0xaf46678e21c8e900,0x27ceef06a9406188, 0xaf46678e21c8e900,0x27ceef06a9406188,
    0x60f7de4929be9700,0x26b1980f6ff8d146, 0x60f7de4929be9700,0x26b1980f6ff8d146,
    0x4e3df383cdbe700,0xa1467a9d997e42a5, 0x4e3df383cdbe700,0xa1467a9d997e42a5,
    0x3fbc27a49b188300,0xb231aa2916950e8d, 0x3fbc27a49b188300,0xb231aa2916950e8d,
    0x1b367558436e2d00,0x9fb2f1dcc7eaa984, 0x1b367558436e2d00,0x9fb2f1dcc7eaa984,
    0xd773258156f2a400,0xa50157f32480d672, 0xd773258156f2a400,0xa50157f32480d672,
    0xc616a171b767d000,0x4f9f28f83eee5989, 0xc616a171b767d000,0x4f9f28f83eee5989,
    0x3bada2340f999600,0x6cfaf56358cec157, 0x3bada2340f999600,0x6cfaf56358cec157,
    0x54e03f8bdf6bb400,0x9420ff4b1fab74c0, 0x54e03f8bdf6bb400,0x9420ff4b1fab74c0,
    0x25b24fd8fd6a9700,0x6cfb0691b423de49, 0x25b24fd8fd6a9700,0x6cfb0691b423de49,
    0x11e685726394f700,0x936407f0e1167582, 0x11e685726394f700,0x936407f0e1167582,
    0xd942ba21f8639b00,0x811ae279a03bc358, 0xd942ba21f8639b00,0x811ae279a03bc358,
    0xad6d67a70acac000,0xa96963a30ecec404, 0xad6d67a70acac000,0xa96963a30ecec404,
    0xcd6510b875dda800,0xf45c29814ce49139, 0xcd6510b875dda800,0xf45c29814ce49139,
    0x7daae235489fd700,0x92450ddaa77038ef, 0x7daae235489fd700,0x92450ddaa77038ef,
    0x70676b7c0c1b1700,0x8f989483f3e4e8ff, 0x70676b7c0c1b1700,0x8f989483f3e4e8ff,
    0xb925ce52eb779c00,0xc955be229b07ec70, 0xb925ce52eb779c00,0xc955be229b07ec70,
    0x209e3e8eae10b00,0xb4bf555e5c57bdb6, 0x209e3e8eae10b00,0xb4bf555e5c57bdb6,
    0x65792c3c5945100,0x85d411404617d283, 0x65792c3c5945100,0x85d411404617d283,
    0xcadf2a3ff5e01500,0x411e4f13b2edbce, 0xcadf2a3ff5e01500,0x411e4f13b2edbce,
    0x8a14af31bb259e00,0xcc52e977fd63d846, 0x8a14af31bb259e00,0xcc52e977fd63d846,
    0x63d67cc9aa1fb500,0xab1eb40162d77dc8, 0x63d67cc9aa1fb500,0xab1eb40162d77dc8,
    0x87f81966e19e7f00,0xc4bb5a25a2dd3c43, 0x87f81966e19e7f00,0xc4bb5a25a2dd3c43,
    0xbb59be5ce705e200,0xae80fed56b453b1, 0xbb59be5ce705e200,0xae80fed56b453b1,
    0x3137040233350600,0x696f5c5a6b6d5e58, 0x3137040233350600,0x696f5c5a6b6d5e58,
    0x3e8168d7e956bf00,0x219e77c8f649a01f, 0x3e8168d7e956bf00,0x219e77c8f649a01f,
    0xb3ca1d64d7ae7900,0x2a5384fd4e37e099, 0xb3ca1d64d7ae7900,0x2a5384fd4e37e099,
    0xd6eba5984e733d00,0x38054b76a09dd3ee, 0xd6eba5984e733d00,0x38054b76a09dd3ee,
    0xcdcd6868a5a50000,0x1818bdbd7070d5d5, 0xcdcd6868a5a50000,0x1818bdbd7070d5d5,
    0x362a405c6a761c00,0x130f65794f533925, 0x362a405c6a761c00,0x130f65794f533925,
    0x3b0ad9e8d3e23100,0x774695a49fae7d4c, 0x3b0ad9e8d3e23100,0x774695a49fae7d4c,
    0x4ef5a01b55eebb00,0x2b9ec5719a2f74c, 0x4ef5a01b55eebb00,0x2b9ec5719a2f74c,
    0xf344b80ffc4bb700,0xa81fe354a710ec5b, 0xf344b80ffc4bb700,0xa81fe354a710ec5b,
    0xa0d9d9a90970700,0x6166f6f1fbfc6c6b, 0xa0d9d9a90970700,0x6166f6f1fbfc6c6b,
    0xec0c3cdc30d0e000,0x47a797779b7b4bab, 0xec0c3cdc30d0e000,0x47a797779b7b4bab,
    0x27a07ef9de598700,0xa720fe795ed90780, 0x27a07ef9de598700,0xa720fe795ed90780,
    0x6620abed8bcd4600,0x296fe4a2c482094f, 0x6620abed8bcd4600,0x296fe4a2c482094f,
    0x50d42aaefe7a8400,0x3eba44c09014ea6e, 0x50d42aaefe7a8400,0x3eba44c09014ea6e,
    0x27499efed9b7600,0xe0967b0d0f7994e2, 0x27499efed9b7600,0xe0967b0d0f7994e2,
    0x55cf3fa5f06a9a00,0x940efe6431ab5bc1, 0x55cf3fa5f06a9a00,0x940efe6431ab5bc1,
    0xb2fde8a7155a4f00,0x7936236cde9184cb, 0xb2fde8a7155a4f00,0x7936236cde9184cb,
    0x683b5300683b5300,0x4211792a4211792a, 0x683b5300683b5300,0x4211792a4211792a,
    0x2b504b301b607b00,0xf48f94efc4bfa4df, 0x2b504b301b607b00,0xf48f94efc4bfa4df,
    0x982a49fb63d1b200,0xbe0c6fdd45f79426, 0x982a49fb63d1b200,0xbe0c6fdd45f79426,
    0x4604246620624200,0xb5f7d795d391b1f3, 0x4604246620624200,0xb5f7d795d391b1f3,
    0xd88888d800505000,0x65353565bdededbd, 0xd88888d800505000,0x65353565bdededbd,
    0xd7f62504d3f22100,0xbe9f4c6dba9b4869, 0xd7f62504d3f22100,0xbe9f4c6dba9b4869,
    0xf4119a7f8b6ee500,0x39dc57b246a328cd, 0xf4119a7f8b6ee500,0x39dc57b246a328cd,
    0x1cdccb0b17d7c000,0xb47463a3bf7f68a8, 0x1cdccb0b17d7c000,0xb47463a3bf7f68a8,
    0x62bc6fb1d30dde00,0x4da09d7b56bb866, 0x62bc6fb1d30dde00,0x4da09d7b56bb866,
    0x83bbf9c1427a3800,0xf7cf8db5360e4c74, 0x83bbf9c1427a3800,0xf7cf8db5360e4c74,
    0x289915a48c3db100,0xca7bf7466edf53e2, 0x289915a48c3db100,0xca7bf7466edf53e2,
    0x3d6f085a67355200,0xe1b3d486bbe98edc, 0x3d6f085a67355200,0xe1b3d486bbe98edc,
    0x44adea0347aee900,0x34dd9a7337de9970, 0x44adea0347aee900,0x34dd9a7337de9970,
    0x3119163e0f272800,0xe1c9c6eedff7f8d0, 0x3119163e0f272800,0xe1c9c6eedff7f8d0,
    0x605b447f1f243b00,0xd3e8f7ccac9788b3, 0x605b447f1f243b00,0xd3e8f7ccac9788b3,
    0x963eb41c8a22a800,0xfe56dc74e24ac068, 0x963eb41c8a22a800,0xfe56dc74e24ac068,
    0x4577c2f0b5873200,0x7e4cf9cb8ebc093b, 0x4577c2f0b5873200,0x7e4cf9cb8ebc093b,
    0x759a917e0be4ef00,0xbe515ab5c02f24cb, 0x759a917e0be4ef00,0xbe515ab5c02f24cb,
    0xa5a47171d4d5000,0xa5f5e8b8b2e2ffaf, 0xa5a47171d4d5000,0xa5f5e8b8b2e2ffaf,
    0xdfbc7310cfac6300,0x6a09c6a57a19d6b5, 0xdfbc7310cfac6300,0x6a09c6a57a19d6b5,
    0x9d9cb4b528290100,0x58597170edecc4c5, 0x9d9cb4b528290100,0x58597170edecc4c5,
    0x57a8f7085fa0ff00,0x8c732cd3847b24db, 0x57a8f7085fa0ff00,0x8c732cd3847b24db,
    0xeb4bea4aa101a000,0x16b617b75cfc5dfd, 0xeb4bea4aa101a000,0x16b617b75cfc5dfd,
    0x1339e8c2d1fb2a00,0xa18b5a70634998b2, 0x1339e8c2d1fb2a00,0xa18b5a70634998b2,
    };


    alignas(32) const uint64_t beta_mul_32_bm4r[(64 / 4) * 16 * 2] = {
    0x9796d3d245440100,0x8485c0c156571213, 0x9796d3d245440100,0x8485c0c156571213,
    0xe9b9e8b851015000,0x6d3d6c3cd585d484, 0xe9b9e8b851015000,0x6d3d6c3cd585d484,
    0xd6d6b4b462620000,0x74741616c0c0a2a2, 0xd6d6b4b462620000,0x74741616c0c0a2a2,
    0x679fb1492ed6f800,0xbb436d95f20a24dc, 0x679fb1492ed6f800,0xbb436d95f20a24dc,
    0x191914140d0d0000,0x6a6a67677e7e7373, 0x191914140d0d0000,0x6a6a67677e7e7373,
    0xd36077c417a4b300,0x5ae9fe4d9e2d3a89, 0xd36077c417a4b300,0x5ae9fe4d9e2d3a89,
    0x6363ecec8f8f0000,0xf4f47b7b18189797, 0x6363ecec8f8f0000,0xf4f47b7b18189797,
    0x255189fdd8ac7400,0x483ce490b5c1196d, 0x255189fdd8ac7400,0x483ce490b5c1196d,
    0x9191e6e677770000,0x52522525b4b4c3c3, 0x9191e6e677770000,0x52522525b4b4c3c3,
    0x4c7b3e0945723700,0x427530074b7c390e, 0x4c7b3e0945723700,0x427530074b7c390e,
    0xaaaa6464cece0000,0x41418f8f2525ebeb, 0xaaaa6464cece0000,0x41418f8f2525ebeb,
    0x813e6dd253ecbf00,0xfd4211ae2f90c37c, 0x813e6dd253ecbf00,0xfd4211ae2f90c37c,
    0x3f3f686857570000,0xd2d28585babaeded, 0x3f3f686857570000,0xd2d28585babaeded,
    0xe702a643a441e500,0x7d983cd93edb7f9a, 0xe702a643a441e500,0x7d983cd93edb7f9a,
    0x5b5bb6b6eded0000,0xc7c72a2a71719c9c, 0x5b5bb6b6eded0000,0xc7c72a2a71719c9c,
    0xb7e31d49feaa5400,0xd98d732790c43a6e, 0xb7e31d49feaa5400,0xd98d732790c43a6e,
    0x28ea02c2ea28c00,0xd15d73fffd715fd3, 0x28ea02c2ea28c00,0xd15d73fffd715fd3,
    0x3ff772ba854dc800,0x30f87db58a42c70f, 0x3ff772ba854dc800,0x30f87db58a42c70f,
    0xc7584cd3148b9f00,0x897831cdb4450cf, 0xc7584cd3148b9f00,0x897831cdb4450cf,
    0x6ed065dbb50bbe00,0x7bc570cea01eab15, 0x6ed065dbb50bbe00,0x7bc570cea01eab15,
    0xf10575817084f400,0xe81c6c98699ded19, 0xf10575817084f400,0xe81c6c98699ded19,
    0xd7f80827f0df2f00,0xeac5351acde2123d, 0xd7f80827f0df2f00,0xeac5351acde2123d,
    0x8a1b28b933a29100,0xc35261f07aebd849, 0x8a1b28b933a29100,0xc35261f07aebd849,
    0x5e847fa5fb21da00,0x62b84399c71de63c, 0x5e847fa5fb21da00,0x62b84399c71de63c,
    0xe87745da32ad9f00,0x51cefc638b1426b9, 0xe87745da32ad9f00,0x51cefc638b1426b9,
    0x2c37011a362d1b00,0x8893a5be9289bfa4, 0x2c37011a362d1b00,0x8893a5be9289bfa4,
    0x2dca39def314e700,0x17f003e4c92edd3a, 0x2dca39def314e700,0x17f003e4c92edd3a,
    0x7bcfdd6912a6b400,0x9c283a8ef54153e7, 0x7bcfdd6912a6b400,0x9c283a8ef54153e7,
    0xbdff7e3c81c34200,0x6426a7e5581a9bd9, 0xbdff7e3c81c34200,0x6426a7e5581a9bd9,
    0x2d7e6a3914475300,0x1f4c580b26756132, 0x2d7e6a3914475300,0x1f4c580b26756132,
    0xe60dbb50b65deb00,0xc72c9a71977cca21, 0xe60dbb50b65deb00,0xc72c9a71977cca21,
    0xc88d03468ecb4500,0x286de3a66e2ba5e0, 0xc88d03468ecb4500,0x286de3a66e2ba5e0,
    0x60fad44e2eb49a00,0xfe644ad0b02a049e, 0x60fad44e2eb49a00,0xfe644ad0b02a049e,
    0xce83511cd29f4d00,0x400ddf925c11c38e, 0xce83511cd29f4d00,0x400ddf925c11c38e,
    0xb4b76665d1d20300,0x1310c1c27675a4a7, 0xb4b76665d1d20300,0x1310c1c27675a4a7,
    0x5031f293c3a26100,0x5233f091c1a06302, 0x5031f293c3a26100,0x5233f091c1a06302,
    0x96f69cfc6a0a6000,0x5d3d5737a1c1abcb, 0x96f69cfc6a0a6000,0x5d3d5737a1c1abcb,
    0x87cb105cdb974c00,0x155982ce4905de92, 0x87cb105cdb974c00,0x155982ce4905de92,
    0x8c41ea27ab66cd00,0x569b30fd71bc17da, 0x8c41ea27ab66cd00,0x569b30fd71bc17da,
    0x720bdda4d6af7900,0x30499fe694ed3b42, 0x720bdda4d6af7900,0x30499fe694ed3b42,
    0xf41093778367e400,0xa541c226d236b551, 0xf41093778367e400,0xa541c226d236b551,
    0xf3337cbc4f8fc000,0x12d29d5dae6e21e1, 0xf3337cbc4f8fc000,0x12d29d5dae6e21e1,
    0xf8fa8f8d75770200,0xd2d0a5a75f5d282a, 0xf8fa8f8d75770200,0xd2d0a5a75f5d282a,
    0x548315c29641d700,0x67b026f1a572e433, 0x548315c29641d700,0x67b026f1a572e433,
    0x62974abfdd28f500,0xd326fb0e6c9944b1, 0x62974abfdd28f500,0xd326fb0e6c9944b1,
    0x9b0a54c55ecf9100,0x2fbee071ea7b25b4, 0x9b0a54c55ecf9100,0x2fbee071ea7b25b4,
    0x55e5ad1d48f8b000,0x4cfcb40451e1a919, 0x55e5ad1d48f8b000,0x4cfcb40451e1a919,
    0xc127e90fce28e600,0x8d6ba5438264aa4c, 0xc127e90fce28e600,0x8d6ba5438264aa4c,
    0x47b146b6f107f00,0xeb94fb8480ff90ef, 0x47b146b6f107f00,0xeb94fb8480ff90ef,
    0x4e7b1326685d3500,0xe6d3bb8ec0f59da8, 0x4e7b1326685d3500,0xe6d3bb8ec0f59da8,
    0x7b750c0279770e00,0x737d040a717f0608, 0x7b750c0279770e00,0x737d040a717f0608,
    0x2e18380e20163600,0xcff9d9efc1f7d7e1, 0x2e18380e20163600,0xcff9d9efc1f7d7e1,
    0x4a592b3872611300,0x9784f6e5afbccedd, 0x4a592b3872611300,0x9784f6e5afbccedd,
    0x6344654221062700,0x6c4b6a4d2e09280f, 0x6344654221062700,0x6c4b6a4d2e09280f,
    0x74787874000c0c00,0xf7fbfbf7838f8f83, 0x74787874000c0c00,0xf7fbfbf7838f8f83,
    0xebdb8bbb50603000,0x51613101eada8aba, 0xebdb8bbb50603000,0x51613101eada8aba,
    0x73f75adead298400,0x8400ad295ade73f7, 0x73f75adead298400,0x8400ad295ade73f7,
    0xda3f769349ace500,0x9c7930d50feaa346, 0xda3f769349ace500,0x9c7930d50feaa346,
    0xb59c80a91c352900,0xe8c1ddf44168745d, 0xb59c80a91c352900,0xe8c1ddf44168745d,
    0xda328e66bc54e800,0x38d06c845eb60ae2, 0xda328e66bc54e800,0x38d06c845eb60ae2,
    0x30ab6ff4c45f9b00,0xda41851e2eb571ea, 0x30ab6ff4c45f9b00,0xda41851e2eb571ea,
    0x305a4b21117b6a00,0x600a1b71412b3a50, 0x305a4b21117b6a00,0x600a1b71412b3a50,
    0x2830190129311800,0x425a736b435b726a, 0x2830190129311800,0x425a736b435b726a,
    0x79cafa493083b300,0x843707b4cd7e4efd, 0x79cafa493083b300,0x843707b4cd7e4efd,
    0x586cb185dde93400,0xa7934e7a2216cbff, 0x586cb185dde93400,0xa7934e7a2216cbff,
    0x2b3e8792b9ac1500,0x9c8930250e1ba2b7, 0x2b3e8792b9ac1500,0x9c8930250e1ba2b7,
    0x702ffca3d38c5f00,0x4619ca95e5ba6936, 0x702ffca3d38c5f00,0x4619ca95e5ba6936,
    0xed9c7908e5947100,0x4736d3a24f3edbaa, 0xed9c7908e5947100,0x4736d3a24f3edbaa,
    0x3a34bbb58f810e00,0xbcb23d3309078886, 0x3a34bbb58f810e00,0xbcb23d3309078886,
    0x3b45f688b3cd7e00,0xf6883b457e00b3cd, 0x3b45f688b3cd7e00,0xf6883b457e00b3cd,
    0x1bd675b8a36ecd00,0xc30ead607bb615d8, 0x1bd675b8a36ecd00,0xc30ead607bb615d8,
    0xc1f4deeb2a1f3500,0xc1f4deeb2a1f3500, 0xc1f4deeb2a1f3500,0xc1f4deeb2a1f3500,
    0xda9594db014e4f00,0x1d52531cc68988c7, 0xda9594db014e4f00,0x1d52531cc68988c7,
    0x97aa89b4231e3d00,0x54694a77e0ddfec3, 0x97aa89b4231e3d00,0x54694a77e0ddfec3,
    0x80904c5cdccc1000,0xeafa2636b6a67a6a, 0x80904c5cdccc1000,0xeafa2636b6a67a6a,
    0x22c13eddff1ce300,0xcc2fd03311f20dee, 0x22c13eddff1ce300,0xcc2fd03311f20dee,
    0xe0435bf818bba300,0x63c0d87b9b382083, 0xe0435bf818bba300,0x63c0d87b9b382083,
    0x77d92e80f759ae00,0x8a651ff8826d17f, 0x77d92e80f759ae00,0x8a651ff8826d17f,
    0xa7f0184fe8bf5700,0x4215fdaa0d5ab2e5, 0xa7f0184fe8bf5700,0x4215fdaa0d5ab2e5,
    0x238ff65a79d5ac00,0x76daa30f2c80f955, 0x238ff65a79d5ac00,0x76daa30f2c80f955,
    0xa3943c0ba89f3700,0xba8d2512b1862e19, 0xa3943c0ba89f3700,0xba8d2512b1862e19,
    0x7992a54e37dceb00,0xea0136dda44f7893, 0x7992a54e37dceb00,0xea0136dda44f7893,
    0x205e2e50700e7e00,0x3d43334d6d13631d, 0x205e2e50700e7e00,0x3d43334d6d13631d,
    0xe0ce5a7494ba2e00,0x8ba5311fffd1456b, 0xe0ce5a7494ba2e00,0x8ba5311fffd1456b,
    0x2ece81614fafe000,0x1dfdb2527c9cd333, 0x2ece81614fafe000,0x1dfdb2527c9cd333,
    0xf3f7afab585c0400,0xc2c69e9a696d3531, 0xf3f7afab585c0400,0xc2c69e9a696d3531,
    0x4d73615f122c3e00,0x8fb1a39dd0eefcc2, 0x4d73615f122c3e00,0x8fb1a39dd0eefcc2,
    0x716acfd4a5be1b00,0x5348edf6879c3922, 0x716acfd4a5be1b00,0x5348edf6879c3922,
    0x487d3500487d3500,0xc0f5bd88c0f5bd88, 0x487d3500487d3500,0xc0f5bd88c0f5bd88,
    0xba39c447fd7e8300,0x2dae53d06ae91497, 0xba39c447fd7e8300,0x2dae53d06ae91497,
    0x3ee84197a97fd600,0xd701a87e40963fe9, 0x3ee84197a97fd600,0xd701a87e40963fe9,
    0x98fa482ab2d06200,0x553785e77f1dafcd, 0x98fa482ab2d06200,0x553785e77f1dafcd,
    0xd5ea93ac79463f00,0x81bec7f82d126b54, 0xd5ea93ac79463f00,0x81bec7f82d126b54,
    0x23dfb844679bfc00,0xcf0976b48b4d32f, 0x23dfb844679bfc00,0xcf0976b48b4d32f,
    0xecb6b0ea065c5a00,0x7923257f93c9cf95, 0xecb6b0ea065c5a00,0x7923257f93c9cf95,
    0xa0e6480eaee84600,0xe9af0147e7a10f49, 0xa0e6480eaee84600,0xe9af0147e7a10f49,
    0xa1a2191abbb80300,0xd5d66d6ecfcc7774, 0xa1a2191abbb80300,0xd5d66d6ecfcc7774,
    0x9672a444d236e00,0xd8b6fb959cf2bfd1, 0x9672a444d236e00,0xd8b6fb959cf2bfd1,
    0x20d8a25a7a82f800,0x3fb817959a1db23, 0x20d8a25a7a82f800,0x3fb817959a1db23,
    0x48f6803e76c8be00,0x2e90e65810aed866, 0x48f6803e76c8be00,0x2e90e65810aed866,
    0xffebd3c7382c1400,0x77635b4fb0a49c88, 0xffebd3c7382c1400,0x77635b4fb0a49c88,
    0xfce2d5cb37291e00,0x4957607e829cabb5, 0xfce2d5cb37291e00,0x4957607e829cabb5,
    0xa7ff93cb6c345800,0xa9f19dc5623a560e, 0xa7ff93cb6c345800,0xa9f19dc5623a560e,
    0xb7059c2e992bb200,0x74c65fed5ae871c3, 0xb7059c2e992bb200,0x74c65fed5ae871c3,
    0xa1095ef657ffa800,0x5adfa52f35b0ca4, 0xa1095ef657ffa800,0x5adfa52f35b0ca4,
    0x31d8a34a7b92e900,0xbd542fc6f71e658c, 0x31d8a34a7b92e900,0xbd542fc6f71e658c,
    0x97a6fdcc5b6a3100,0x29184372e5d48fbe, 0x97a6fdcc5b6a3100,0x29184372e5d48fbe,
    0x168869f7e17f9e00,0x801eff6177e90896, 0x168869f7e17f9e00,0x801eff6177e90896,
    0xbbdf7216adc96400,0xcaae0367dcb81571, 0xbbdf7216adc96400,0xcaae0367dcb81571,
    0xa50909a500acac00,0xff5353ff5af6f65a, 0xa50909a500acac00,0xff5353ff5af6f65a,
    0x5ce4ff471ba3b800,0x7bfa41c40f8e35b, 0x5ce4ff471ba3b800,0x7bfa41c40f8e35b,
    0x7531d494e1a5400,0x4d19570304501e4a, 0x7531d494e1a5400,0x4d19570304501e4a,
    0xd97ccf6ab316a500,0xeb4efd5881249732, 0xd97ccf6ab316a500,0xeb4efd5881249732,
    0x47f0f34403b4b700,0xbbcbf084ff8fb4c, 0x47f0f34403b4b700,0xbbcbf084ff8fb4c,
    0x7d77c7cdb0ba0a00,0x7379c9c3beb4040e, 0x7d77c7cdb0ba0a00,0x7379c9c3beb4040e,
    0xd4331bfc28cfe700,0x30d7ff18cc2b03e4, 0xd4331bfc28cfe700,0x30d7ff18cc2b03e4,
    0xf2546fc93b9da600,0xf3556ec83a9ca701, 0xf2546fc93b9da600,0xf3556ec83a9ca701,
    0xfc3cb2728e4ec000,0xea2aa4649858d616, 0xfc3cb2728e4ec000,0xea2aa4649858d616,
    0x1a8882100a989200,0x1f8d87150f9d9705, 0x1a8882100a989200,0x1f8d87150f9d9705,
    0xa2d41365c7b17600,0xb7dbacc6e18dfa9, 0xa2d41365c7b17600,0xb7dbacc6e18dfa9,
    0xa66929e6408fcf00,0xe32c6ca305ca8a45, 0xa66929e6408fcf00,0xe32c6ca305ca8a45,
    0x39a7a739009e9e00,0xbd2323bd841a1a84, 0x39a7a739009e9e00,0xbd2323bd841a1a84,
    0xd20f9f42904ddd00,0xb76afa27f528b865, 0xd20f9f42904ddd00,0xb76afa27f528b865,
    0xd02336c515e6f300,0x5ba8bd4e9e6d788b, 0xd02336c515e6f300,0x5ba8bd4e9e6d788b,
    0x6322632241004100,0x92d392d3b0f1b0f1, 0x6322632241004100,0x92d392d3b0f1b0f1,
    0xcd4035b875f88d00,0xea67129f52dfaa27, 0xcd4035b875f88d00,0xea67129f52dfaa27,
    0xf4f21a1ce8ee0600,0xadab4345b1b75f59, 0xf4f21a1ce8ee0600,0xadab4345b1b75f59,
    0x8d80010c818c0d00,0xb6bb3a37bab7363b, 0x8d80010c818c0d00,0xb6bb3a37bab7363b,
    };


}
#endif
