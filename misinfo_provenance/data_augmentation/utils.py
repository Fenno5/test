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

# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""This file include utils functions and variables used by the data Augmentaion.

module.
"""

# List of fonts used on the overlay text class.
FONT_LIST = [
    'Raleway-ExtraBoldItalic.ttf', 'OstrichSansRounded-Medium.ttf',
    'IBMPlexMono-Thin.ttf', 'PlayfairDisplay-BlackItalic.ttf',
    'Raleway-ExtraLightItalic.ttf', 'AlexBrush-Regular.ttf',
    'Raleway-SemiBoldItalic.ttf', 'MontserratAlternates-Italic.ttf',
    'IBMPlexSans-MediumItalic.ttf', 'PlayfairDisplaySC-Black.ttf',
    'IBMPlexSans-LightItalic.ttf', 'Raleway-Bold.ttf',
    'Raleway-LightItalic.ttf', 'OpenSans-ExtraBold.ttf', 'Ubuntu-MI.ttf',
    'IBMPlexMono-Text.ttf', 'Ubuntu-C.ttf', 'IBMPlexSans-Thin.ttf',
    'OstrichSans-Heavy.ttf', 'PlayfairDisplay-Italic.ttf',
    'IBMPlexMono-ExtraLight.ttf', 'Pacifico.ttf',
    'SourceSansPro-SemiboldIt.ttf', 'Lobster_1.3.ttf',
    'Montserrat-ExtraLightItalic.ttf', 'OpenSans-SemiboldItalic.ttf',
    'WC_Rhesus_A_Bta.ttf', 'SolveigDisplay-Italic.ttf',
    'IBMPlexSerif-Italic.ttf', 'MontserratAlternates-Light.ttf',
    'modernpics.ttf', 'Ubuntu-L.ttf', 'heydings_icons.ttf',
    'IBMPlexSerif-ThinItalic.ttf', 'Montserrat-Medium.ttf',
    'IBMPlexMono-ThinItalic.ttf', 'IBMPlexSans-SemiBold.ttf',
    'Montserrat-BlackItalic.ttf', 'SourceSansPro-BoldIt.ttf',
    'berkshireswash-regular.ttf', 'IBMPlexMono-Regular.ttf',
    'Montserrat-MediumItalic.ttf', 'IBMPlexSerif-MediumItalic.ttf',
    'MontserratAlternates-ExtraBoldItalic.ttf', 'Ubuntu-B.ttf',
    'Raleway-BoldItalic.ttf', 'Chunkfive.ttf', 'DavysDingbats.ttf',
    'IBMPlexMono-MediumItalic.ttf', 'OpenSans-BoldItalic.ttf',
    'MontserratAlternates-ExtraLightItalic.ttf', 'SirucaPictograms1.1_.ttf',
    'MountainsofChristmas.ttf', 'MontserratAlternates-ThinItalic.ttf',
    'Titillium-SemiboldUpright.ttf', 'Titillium-BoldItalic.ttf',
    'IBMPlexSerif-SemiBold.ttf', 'Ubuntu-LI.ttf',
    'MontserratAlternates-Black.ttf', 'WC_Rhesus_B_Bta.ttf',
    'Raleway-Regular.ttf', 'IBMPlexSans-Regular.ttf', 'Montserrat-Thin.ttf',
    'GreatVibes-Regular.ttf', 'KaushanScript-Regular.ttf', 'Prata-Regular.ttf',
    'PlayfairDisplay-Bold.ttf', 'Raleway-Italic.ttf',
    'MontserratAlternates-Thin.ttf', 'OstrichSans-Black.ttf',
    'ElsieSwashCaps-Regular.ttf', 'IBMPlexSerif-BoldItalic.ttf',
    'Kalocsai_Flowers.ttf', 'Titillium-LightItalic.ttf',
    'Titillium-SemiboldItalic.ttf', 'SolveigBold.ttf', 'blackjack.ttf',
    'SourceSansPro-ExtraLightIt.ttf', 'OpenSans-Regular.ttf',
    'IBMPlexMono-SemiBold.ttf', 'SourceSansPro-LightIt.ttf',
    'DancingScript-Regular.ttf', 'Montserrat-Light.ttf',
    'OstrichSans-Medium.ttf', 'IBMPlexMono-BoldItalic.ttf',
    'WC_Sold_Out_B_Bta.ttf', 'IBMPlexSerif-ExtraLight.ttf',
    'IBMPlexSans-ThinItalic.ttf', 'Allura-Regular.ttf', 'OstrichSans-Bold.ttf',
    'MontserratAlternates-SemiBold.ttf', 'SourceSansPro-Black.ttf',
    'Sofia-Regular.ttf', 'heydings_controls.ttf', 'IBMPlexSans-Light.ttf',
    'Ubuntu-RI.ttf', 'PlayfairDisplaySC-Regular.ttf', 'symbol-signs.ttf',
    'Raleway-BlackItalic.ttf', 'OpenSans-Bold.ttf', 'IBMPlexSerif-Bold.ttf',
    'WCSoldOutABta.ttf', 'IBMPlexSans-BoldItalic.ttf',
    'OpenSans-ExtraBoldItalic.ttf', 'SolveigText-Italic.ttf',
    'SolveigDemiBold-Italic.ttf', 'IBMPlexSerif-SemiBoldItalic.ttf',
    'LeagueSpartan-Bold.ttf', 'Caviar_Dreams_Bold.ttf',
    'Montserrat-ExtraBoldItalic.ttf', 'Titillium-Thin.ttf',
    'MontserratAlternates-Bold.ttf', 'OpenSans-LightItalic.ttf',
    'infini-italique.ttf', 'TypeMyMusic_1.1.ttf',
    'MontserratAlternates-ExtraLight.ttf', 'IBMPlexSans-ExtraLightItalic.ttf',
    'Titillium-LightUpright.ttf', 'Montserrat-Regular.ttf',
    'IBMPlexSans-TextItalic.ttf', 'IBMPlexSerif-Text.ttf',
    'IBMPlexSans-Medium.ttf', 'infini-picto.ttf', 'ostrich-regular.ttf',
    'IBMPlexSans-ExtraLight.ttf', 'Titillium-Regular.ttf', 'SolveigText.ttf',
    'Entypo.ttf', 'PlayfairDisplay-Black.ttf', 'IBMPlexSerif-TextItalic.ttf',
    'Raleway-Black.ttf', 'Montserrat-ExtraLight.ttf', 'IBMPlexSans-Text.ttf',
    'PlayfairDisplaySC-BoldItalic.ttf', 'IBMPlexSerif-Medium.ttf',
    'CaviarDreams.ttf', 'IBMPlexMono-Light.ttf', 'SourceSansPro-Semibold.ttf',
    'IBMPlexSerif-LightItalic.ttf', 'SolveigDemiBold.ttf',
    'Titillium-ThinItalic.ttf', 'OpenSans-Semibold.ttf',
    'Titillium-ThinUpright.ttf', 'Titillium-RegularUpright.ttf',
    'WC_Sold_Out_C_Bta.ttf', 'Montserrat-Bold.ttf', 'IBMPlexMono-Medium.ttf',
    'PlayfairDisplaySC-Italic.ttf', 'Montserrat-ExtraBold.ttf',
    'Titillium-BoldUpright.ttf', 'CaviarDreams_Italic.ttf',
    'PlayfairDisplay-BoldItalic.ttf', 'Montserrat-Black.ttf',
    'IBMPlexSerif-Regular.ttf', 'IBMPlexMono-ExtraLightItalic.ttf',
    'ElsieSwashCaps-Black.ttf', 'Montserrat-ThinItalic.ttf',
    'MontserratAlternates-MediumItalic.ttf', 'IBMPlexMono-Bold.ttf',
    'Ubuntu-R.ttf', 'Raleway-ExtraLight.ttf', 'OstrichSans-Light.ttf',
    'Raleway-Medium.ttf', 'SourceSansPro-Regular.ttf', 'Ubuntu-M.ttf',
    'Montserrat-SemiBoldItalic.ttf', 'IBMPlexSerif-Thin.ttf',
    'PlayfairDisplaySC-Bold.ttf', 'Titillium-Semibold.ttf',
    'Raleway-MediumItalic.ttf', 'Titillium-RegularItalic.ttf', 'Outgunned.ttf',
    'SolveigBold-Italic.ttf', 'SourceSansPro-It.ttf', 'Elsie-Black.ttf',
    'OpenSans-Light.ttf', 'SourceSansPro-ExtraLight.ttf', 'Elsie-Regular.ttf',
    'Raleway-Thin.ttf', 'PlayfairDisplaySC-BlackItalic.ttf',
    'Montserrat-Italic.ttf', 'IBMPlexSerif-ExtraLightItalic.ttf',
    'IBMPlexSans-Bold.ttf', 'Montserrat-BoldItalic.ttf',
    'IBMPlexSans-SemiBoldItalic.ttf', 'GrandHotel-Regular.ttf',
    'Raleway-ExtraBold.ttf', 'IBMPlexMono-SemiBoldItalic.ttf',
    'OstrichSansDashed-Medium.ttf', 'Titillium-Black.ttf', 'Titillium-Bold.ttf',
    'MontserratAlternates-ExtraBold.ttf', 'IBMPlexSerif-Light.ttf',
    'IBMPlexSans-Italic.ttf', 'Ubuntu-BI.ttf', 'Titillium-Light.ttf',
    'Montserrat-LightItalic.ttf', 'Raleway-Light.ttf',
    'IBMPlexMono-TextItalic.ttf', 'Raleway-ThinItalic.ttf',
    'MontserratAlternates-LightItalic.ttf', 'SourceSansPro-Light.ttf',
    'infini-gras.ttf', 'Montserrat-SemiBold.ttf', 'cac_champagne.ttf',
    'Impact.ttf', 'MontserratAlternates-BlackItalic.ttf',
    'MontserratAlternates-Regular.ttf', 'Windsong.ttf',
    'IBMPlexMono-Italic.ttf', 'OpenSans-Italic.ttf', 'SourceSansPro-Bold.ttf',
    'MontserratAlternates-Medium.ttf',
    'MontserratAlternates-SemiBoldItalic.ttf', 'PlayfairDisplay-Regular.ttf',
    'SolveigDisplay.ttf', 'IBMPlexMono-LightItalic.ttf',
    'SourceSansPro-BlackIt.ttf', 'Raleway-SemiBold.ttf',
    'CaviarDreams_BoldItalic.ttf', 'infini-romain.ttf'
]

# List of emoji images used on the overlay emoji class.
EMOJI_LIST = [
    'animals_and_nature/crocodile.png', 'animals_and_nature/elephant.png',
    'animals_and_nature/dog_face.png', 'animals_and_nature/monkey_face.png',
    'animals_and_nature/cow_face.png', 'animals_and_nature/pig.png',
    'animals_and_nature/mouse.png', 'animals_and_nature/bird.png',
    'animals_and_nature/rat.png', 'animals_and_nature/mouse_face.png',
    'animals_and_nature/monkey.png', 'animals_and_nature/turtle.png',
    'animals_and_nature/dragon_face.png', 'animals_and_nature/dolphin.png',
    'animals_and_nature/rabbit_face.png', 'animals_and_nature/ram.png',
    'animals_and_nature/leopard.png', 'animals_and_nature/penguin.png',
    'animals_and_nature/tiger_face.png', 'animals_and_nature/rose.png',
    'animals_and_nature/panda.png', 'animals_and_nature/rabbit.png',
    'animals_and_nature/four_leaf_clover.png',
    'animals_and_nature/pig_face.png', 'animals_and_nature/tiger.png',
    'animals_and_nature/frog.png', 'animals_and_nature/bouquet.png',
    'animals_and_nature/camel.png', 'animals_and_nature/wolf.png',
    'animals_and_nature/horse.png', 'animals_and_nature/deciduous_tree.png',
    'animals_and_nature/water_buffalo.png',
    'animals_and_nature/spiral_shell.png', 'animals_and_nature/ewe.png',
    'animals_and_nature/front_facing_baby_chick.png',
    'animals_and_nature/snail.png', 'animals_and_nature/chicken.png',
    'animals_and_nature/paw_prints.png', 'animals_and_nature/honeybee.png',
    'animals_and_nature/ant.png', 'animals_and_nature/bug.png',
    'animals_and_nature/seedling.png', 'animals_and_nature/ox.png',
    'animals_and_nature/cactus.png', 'animals_and_nature/cherry_blossom.png',
    'animals_and_nature/dashing_away.png',
    'animals_and_nature/two_hump_camel.png', 'animals_and_nature/palm_tree.png',
    'animals_and_nature/dizzy.png', 'animals_and_nature/cat_face.png',
    'animals_and_nature/fish.png', 'animals_and_nature/tulip.png',
    'animals_and_nature/snake.png', 'animals_and_nature/goat.png',
    'animals_and_nature/blossom.png', 'animals_and_nature/evergreen_tree.png',
    'animals_and_nature/whale.png', 'animals_and_nature/octopus.png',
    'animals_and_nature/hibiscus.png', 'animals_and_nature/tropical_fish.png',
    'animals_and_nature/lady_beetle.png',
    'animals_and_nature/sweat_droplets.png', 'animals_and_nature/cow.png',
    'animals_and_nature/blowfish.png', 'animals_and_nature/spouting_whale.png',
    'animals_and_nature/fallen_leaf.png', 'animals_and_nature/hamster.png',
    'animals_and_nature/pig_nose.png', 'animals_and_nature/collision.png',
    'animals_and_nature/dragon.png', 'animals_and_nature/poodle.png',
    'animals_and_nature/sheaf_of_rice.png', 'animals_and_nature/droplet.png',
    'animals_and_nature/koala.png', 'animals_and_nature/baby_chick.png',
    'animals_and_nature/hatching_chick.png', 'animals_and_nature/rooster.png',
    'animals_and_nature/boar.png', 'animals_and_nature/herb.png',
    'animals_and_nature/dog.png', 'animals_and_nature/cat.png',
    'animals_and_nature/horse_face.png', 'animals_and_nature/sunflower.png',
    'animals_and_nature/leaf_fluttering_in_wind.png',
    'animals_and_nature/bear.png', 'animals_and_nature/maple_leaf.png',
    'people/tongue.png', 'people/waving_hand.png', 'people/open_hands.png',
    'people/backhand_index_pointing_left.png',
    'people/person_mountain_biking.png', 'people/construction_worker.png',
    'people/bride_with_veil.png', 'people/person_raising_hand.png',
    'people/ear.png', 'people/backhand_index_pointing_down.png',
    'people/oncoming_fist.png', 'people/folded_hands.png',
    'people/person_wearing_turban.png', 'people/top_hat.png',
    'people/backhand_index_pointing_up.png',
    'people/person_getting_massage.png', 'people/ok_hand.png',
    'people/nail_polish.png', 'people/baby.png',
    'people/person_rowing_boat.png', 'people/person_walking.png',
    'people/raised_hand.png', 'people/woman_and_man_holding_hands.png',
    'people/baby_angel.png', 'people/busts_in_silhouette.png',
    'people/person_gesturing_ok.png', 'people/people_with_bunny_ears.png',
    'people/boy.png', 'people/girl.png', 'people/men_holding_hands.png',
    'people/old_man.png', 'people/footprints.png',
    'people/man_with_skullcap.png', 'people/thumbs_up.png',
    'people/index_pointing_up.png', 'people/nose.png', 'people/man.png',
    'people/person_frowning.png', 'people/santa_claus.png',
    'people/man_running.png', 'people/woman_dancing.png',
    'people/raised_fist.png', 'people/person_taking_bath.png',
    'people/bust_in_silhouette.png', 'people/raising_hands.png',
    'people/guard.png', 'people/person_pouting.png',
    'people/person_getting_haircut.png', 'people/person_gesturing_no.png',
    'people/eyes.png', 'people/person_bowing.png',
    'people/backhand_index_pointing_right.png', 'people/flexed_biceps.png',
    'people/police_officer.png', 'people/person_blond_hair.png',
    'people/clapping_hands.png', 'people/thumbs_down.png',
    'people/victory_hand.png', 'people/old_woman.png', 'people/princess.png',
    'people/mouth.png', 'people/kiss.png', 'people/briefcase.png',
    'people/family.png', 'people/person_tipping_hand.png', 'people/woman.png',
    'people/person_biking.png', 'people/women_holding_hands.png',
    'people/pile_of_poo.png', 'people/couple_with_heart.png',
    'activity/fishing_pole.png', 'activity/pool_8_ball.png',
    'activity/microphone.png', 'activity/spade_suit.png',
    'activity/circus_tent.png', 'activity/tennis.png', 'activity/guitar.png',
    'activity/direct_hit.png', 'activity/pine_decoration.png',
    'activity/club_suit.png', 'activity/man_swimming.png',
    'activity/headphone.png', 'activity/soccer_ball.png',
    'activity/party_popper.png', 'activity/horse_racing.png',
    'activity/moon_viewing_ceremony.png', 'activity/fireworks.png',
    'activity/skier.png', 'activity/wrapped_gift.png',
    'activity/heart_suit.png', 'activity/crystal_ball.png',
    'activity/clapper_board.png', 'activity/trumpet.png',
    'activity/confetti_ball.png', 'activity/sparkles.png',
    'activity/man_surfing.png', 'activity/skis.png',
    'activity/artist_palette.png', 'activity/musical_keyboard.png',
    'activity/rugby_football.png', 'activity/japanese_dolls.png',
    'activity/flag_in_hole.png', 'activity/bowling.png',
    'activity/baseball.png', 'activity/performing_arts.png',
    'activity/diamond_suit.png', 'activity/jack_o_lantern.png',
    'activity/american_football.png', 'activity/basketball.png',
    'activity/ticket.png', 'activity/balloon.png', 'activity/game_die.png',
    'activity/trophy.png', 'activity/wind_chime.png', 'activity/violin.png',
    'activity/christmas_tree.png', 'activity/running_shirt.png',
    'activity/saxophone.png', 'activity/video_game.png',
    'activity/slot_machine.png', 'activity/ribbon.png',
    'activity/tanabata_tree.png', 'activity/carp_streamer.png',
    'activity/sparkler.png', 'activity/musical_score.png', 'symbols/joker.png',
    'symbols/scorpio.png', 'symbols/blue_circle.png', 'symbols/capricorn.png',
    'symbols/white_circle.png', 'symbols/atm.png', 'symbols/zzz.png',
    'symbols/prohibited.png', 'symbols/passport_control.png',
    'symbols/japanese_bargain_button.png', 'symbols/input_symbols.png',
    'symbols/japanese_monthly_amount_button.png',
    'symbols/left_right_arrow.png', 'symbols/shuffle_tracks_button.png',
    'symbols/aquarius.png', 'symbols/copyright.png', 'symbols/sagittarius.png',
    'symbols/right_arrow.png', 'symbols/eight_spoked_asterisk.png',
    'symbols/fast_up_button.png', 'symbols/cross_mark.png',
    'symbols/downwards_button.png', 'symbols/b_button_blood_type.png',
    'symbols/end_arrow.png', 'symbols/red_circle.png',
    'symbols/baggage_claim.png', 'symbols/up_left_arrow.png',
    'symbols/vs_button.png', 'symbols/division_sign.png',
    'symbols/black_square_button.png', 'symbols/keycap_10.png',
    'symbols/recycling_symbol.png', 'symbols/anger_symbol.png',
    'symbols/input_latin_lowercase.png', 'symbols/check_mark_button.png',
    'symbols/warning.png', 'symbols/wavy_dash.png',
    'symbols/litter_in_bin_sign.png', 'symbols/red_triangle_pointed_up.png',
    'symbols/eight_pointed_star.png', 'symbols/speech_balloon.png',
    'symbols/ophiuchus.png', 'symbols/multiplication_sign.png',
    'symbols/japanese_prohibited_button.png', 'symbols/exclamation_mark.png',
    'symbols/cancer.png', 'symbols/free_button.png',
    'symbols/double_curly_loop.png', 'symbols/wheelchair_symbol.png',
    'symbols/large_orange_diamond.png',
    'symbols/counterclockwise_arrows_button.png', 'symbols/name_badge.png',
    'symbols/up_down_arrow.png', 'symbols/japanese_application_button.png',
    'symbols/ng_button.png', 'symbols/cl_button.png', 'symbols/play_button.png',
    'symbols/black_large_square.png', 'symbols/japanese_secret_button.png',
    'symbols/pisces.png', 'symbols/registered.png', 'symbols/up_button.png',
    'symbols/check_box_with_check.png', 'symbols/currency_exchange.png',
    'symbols/input_numbers.png', 'symbols/thought_balloon.png',
    'symbols/gemini.png', 'symbols/diamond_with_a_dot.png',
    'symbols/dim_button.png', 'symbols/reverse_button.png',
    'symbols/white_medium_square.png', 'symbols/japanese_discount_button.png',
    'symbols/black_medium_square.png', 'symbols/soon_arrow.png',
    'symbols/white_large_square.png', 'symbols/japanese_vacancy_button.png',
    'symbols/right_arrow_curving_up.png', 'symbols/white_small_square.png',
    'symbols/cool_button.png', 'symbols/japanese_symbol_for_beginner.png',
    'symbols/left_luggage.png', 'symbols/sparkle.png', 'symbols/libra.png',
    'symbols/japanese_not_free_of_charge_button.png',
    'symbols/mobile_phone_off.png', 'symbols/heavy_dollar_sign.png',
    'symbols/hundred_points.png', 'symbols/japanese_here_button.png',
    'symbols/no_mobile_phones.png', 'symbols/no_bicycles.png',
    'symbols/cinema.png', 'symbols/large_blue_diamond.png',
    'symbols/trade_mark.png', 'symbols/white_exclamation_mark.png',
    'symbols/white_flower.png', 'symbols/id_button.png',
    'symbols/sos_button.png', 'symbols/dotted_six_pointed_star.png',
    'symbols/upwards_button.png', 'symbols/plus_sign.png',
    'symbols/down_right_arrow.png',
    'symbols/japanese_open_for_business_button.png',
    'symbols/o_button_blood_type.png', 'symbols/japanese_reserved_button.png',
    'symbols/mahjong_red_dragon.png', 'symbols/restroom.png',
    'symbols/water_closet.png', 'symbols/cross_mark_button.png',
    'symbols/virgo.png', 'symbols/repeat_button.png',
    'symbols/white_question_mark.png', 'symbols/up_right_arrow.png',
    'symbols/fast_down_button.png', 'symbols/p_button.png', 'symbols/aries.png',
    'symbols/vibration_mode.png', 'symbols/musical_notes.png',
    'symbols/loudspeaker.png', 'symbols/left_arrow.png',
    'symbols/children_crossing.png', 'symbols/radio_button.png',
    'symbols/mens_room.png', 'symbols/trident_emblem.png',
    'symbols/customs.png', 'symbols/bright_button.png',
    'symbols/curly_loop.png', 'symbols/circled_m.png',
    'symbols/chart_increasing_with_yen.png', 'symbols/fast_forward_button.png',
    'symbols/musical_note.png', 'symbols/information.png',
    'symbols/exclamation_question_mark.png', 'symbols/small_blue_diamond.png',
    'symbols/leo.png', 'symbols/ab_button_blood_type.png',
    'symbols/keycap_number_sign.png', 'symbols/question_mark.png',
    'symbols/megaphone.png', 'symbols/repeat_single_button.png',
    'symbols/red_triangle_pointed_down.png', 'symbols/up_arrow.png',
    'symbols/flower_playing_cards.png', 'symbols/minus_sign.png',
    'symbols/right_arrow_curving_left.png',
    'symbols/japanese_passing_grade_button.png',
    'symbols/white_medium_small_square.png', 'symbols/back_arrow.png',
    'symbols/clockwise_vertical_arrows.png', 'symbols/baby_symbol.png',
    'symbols/non_potable_water.png', 'symbols/no_pedestrians.png',
    'symbols/no_entry.png', 'symbols/double_exclamation_mark.png',
    'symbols/check_mark.png', 'symbols/white_square_button.png',
    'symbols/japanese_congratulations_button.png', 'symbols/on_arrow.png',
    'symbols/black_circle.png', 'symbols/antenna_bars.png',
    'symbols/new_button.png', 'symbols/input_latin_letters.png',
    'symbols/down_left_arrow.png', 'symbols/japanese_free_of_charge_button.png',
    'symbols/no_one_under_eighteen.png', 'symbols/fast_reverse_button.png',
    'symbols/top_arrow.png', 'symbols/no_littering.png',
    'symbols/a_button_blood_type.png', 'symbols/ok_button.png',
    'symbols/small_orange_diamond.png', 'symbols/hollow_red_circle.png',
    'symbols/down_arrow.png', 'symbols/japanese_acceptable_button.png',
    'symbols/right_arrow_curving_down.png', 'symbols/no_smoking.png',
    'symbols/black_medium_small_square.png',
    'symbols/input_latin_uppercase.png', 'symbols/left_arrow_curving_right.png',
    'symbols/japanese_service_charge_button.png',
    'symbols/japanese_no_vacancy_button.png', 'symbols/black_small_square.png',
    'symbols/taurus.png', 'symbols/womens_room.png',
    'symbols/potable_water.png', 'symbols/part_alternation_mark.png',
    'food_and_drink/cooked_rice.png', 'food_and_drink/pineapple.png',
    'food_and_drink/doughnut.png', 'food_and_drink/meat_on_bone.png',
    'food_and_drink/ear_of_corn.png', 'food_and_drink/hot_beverage.png',
    'food_and_drink/bread.png', 'food_and_drink/tomato.png',
    'food_and_drink/cookie.png', 'food_and_drink/oden.png',
    'food_and_drink/melon.png', 'food_and_drink/ice_cream.png',
    'food_and_drink/baby_bottle.png', 'food_and_drink/bento_box.png',
    'food_and_drink/rice_ball.png', 'food_and_drink/sushi.png',
    'food_and_drink/hamburger.png', 'food_and_drink/soft_ice_cream.png',
    'food_and_drink/custard.png', 'food_and_drink/candy.png',
    'food_and_drink/peach.png', 'food_and_drink/rice_cracker.png',
    'food_and_drink/mushroom.png', 'food_and_drink/steaming_bowl.png',
    'food_and_drink/clinking_beer_mugs.png', 'food_and_drink/birthday_cake.png',
    'food_and_drink/french_fries.png', 'food_and_drink/wine_glass.png',
    'food_and_drink/shaved_ice.png', 'food_and_drink/tropical_drink.png',
    'food_and_drink/honey_pot.png', 'food_and_drink/watermelon.png',
    'food_and_drink/grapes.png', 'food_and_drink/eggplant.png',
    'food_and_drink/pot_of_food.png', 'food_and_drink/pizza.png',
    'food_and_drink/lemon.png', 'food_and_drink/cocktail_glass.png',
    'food_and_drink/green_apple.png', 'food_and_drink/fish_cake_with_swirl.png',
    'food_and_drink/kitchen_knife.png', 'food_and_drink/chocolate_bar.png',
    'food_and_drink/curry_rice.png', 'food_and_drink/banana.png',
    'food_and_drink/strawberry.png', 'food_and_drink/fried_shrimp.png',
    'food_and_drink/shortcake.png', 'food_and_drink/beer_mug.png',
    'food_and_drink/lollipop.png', 'food_and_drink/roasted_sweet_potato.png',
    'food_and_drink/red_apple.png', 'food_and_drink/spaghetti.png',
    'food_and_drink/fork_and_knife.png', 'food_and_drink/tangerine.png',
    'food_and_drink/cherries.png', 'food_and_drink/poultry_leg.png',
    'food_and_drink/pear.png', 'food_and_drink/teacup_without_handle.png',
    'food_and_drink/dango.png', 'food_and_drink/cooking.png',
    'food_and_drink/sake.png', 'food_and_drink/chestnut.png',
    'travel_and_places/ship.png', 'travel_and_places/sun_behind_cloud.png',
    'travel_and_places/barber_pole.png', 'travel_and_places/wedding.png',
    'travel_and_places/oncoming_taxi.png', 'travel_and_places/sun.png',
    'travel_and_places/new_moon_face.png', 'travel_and_places/hotel.png',
    'travel_and_places/shibuya.png', 'travel_and_places/convenience_store.png',
    'travel_and_places/station.png', 'travel_and_places/factory.png',
    'travel_and_places/twelve_thirty.png',
    'travel_and_places/oncoming_automobile.png',
    'travel_and_places/mount_fuji.png', 'travel_and_places/church.png',
    'travel_and_places/crescent_moon.png', 'travel_and_places/automobile.png',
    'travel_and_places/castle.png', 'travel_and_places/eight_thirty.png',
    'travel_and_places/seat.png', 'travel_and_places/eleven_oclock.png',
    'travel_and_places/house_with_garden.png',
    'travel_and_places/eight_oclock.png',
    'travel_and_places/waning_gibbous_moon.png',
    'travel_and_places/seven_oclock.png', 'travel_and_places/tram.png',
    'travel_and_places/four_thirty.png', 'travel_and_places/tram_car.png',
    'travel_and_places/nine_thirty.png', 'travel_and_places/twelve_oclock.png',
    'travel_and_places/bicycle.png', 'travel_and_places/fire.png',
    'travel_and_places/five_thirty.png',
    'travel_and_places/globe_showing_europe_africa.png',
    'travel_and_places/last_quarter_moon.png',
    'travel_and_places/bullet_train.png', 'travel_and_places/bus_stop.png',
    'travel_and_places/hot_springs.png', 'travel_and_places/sunrise.png',
    'travel_and_places/high_speed_train.png',
    'travel_and_places/sunrise_over_mountains.png',
    'travel_and_places/rocket.png', 'travel_and_places/one_thirty.png',
    'travel_and_places/department_store.png',
    'travel_and_places/fire_engine.png', 'travel_and_places/two_thirty.png',
    'travel_and_places/globe_showing_americas.png',
    'travel_and_places/foggy.png', 'travel_and_places/ambulance.png',
    'travel_and_places/rainbow.png',
    'travel_and_places/snowman_without_snow.png',
    'travel_and_places/three_oclock.png',
    'travel_and_places/waxing_crescent_moon.png',
    'travel_and_places/sport_utility_vehicle.png',
    'travel_and_places/map_of_japan.png',
    'travel_and_places/hourglass_not_done.png',
    'travel_and_places/helicopter.png',
    'travel_and_places/globe_showing_asia_australia.png',
    'travel_and_places/globe_with_meridians.png',
    'travel_and_places/closed_umbrella.png',
    'travel_and_places/office_building.png', 'travel_and_places/sunset.png',
    'travel_and_places/oncoming_police_car.png',
    'travel_and_places/one_oclock.png', 'travel_and_places/mountain_railway.png',
    'travel_and_places/construction.png', 'travel_and_places/police_car.png',
    'travel_and_places/railway_car.png', 'travel_and_places/five_oclock.png',
    'travel_and_places/six_oclock.png',
    'travel_and_places/suspension_railway.png',
    'travel_and_places/three_thirty.png', 'travel_and_places/love_hotel.png',
    'travel_and_places/trolleybus.png', 'travel_and_places/two_oclock.png',
    'travel_and_places/house.png', 'travel_and_places/shooting_star.png',
    'travel_and_places/minibus.png', 'travel_and_places/six_thirty.png',
    'travel_and_places/full_moon.png', 'travel_and_places/full_moon_face.png',
    'travel_and_places/cityscape_at_dusk.png', 'travel_and_places/tractor.png',
    'travel_and_places/aerial_tramway.png',
    'travel_and_places/carousel_horse.png', 'travel_and_places/fuel_pump.png',
    'travel_and_places/metro.png', 'travel_and_places/sun_with_face.png',
    'travel_and_places/sailboat.png', 'travel_and_places/watch.png',
    'travel_and_places/statue_of_liberty.png',
    'travel_and_places/bridge_at_night.png', 'travel_and_places/star.png',
    'travel_and_places/four_oclock.png', 'travel_and_places/hourglass_done.png',
    'travel_and_places/high_voltage.png',
    'travel_and_places/european_post_office.png',
    'travel_and_places/water_wave.png', 'travel_and_places/anchor.png',
    'travel_and_places/night_with_stars.png', 'travel_and_places/school.png',
    'travel_and_places/waxing_gibbous_moon.png',
    'travel_and_places/light_rail.png', 'travel_and_places/fountain.png',
    'travel_and_places/monorail.png', 'travel_and_places/japanese_castle.png',
    'travel_and_places/japanese_post_office.png',
    'travel_and_places/first_quarter_moon.png',
    'travel_and_places/tokyo_tower.png',
    'travel_and_places/last_quarter_moon_face.png', 'travel_and_places/taxi.png',
    'travel_and_places/bus.png', 'travel_and_places/milky_way.png',
    'travel_and_places/first_quarter_moon_face.png',
    'travel_and_places/glowing_star.png', 'travel_and_places/cyclone.png',
    'travel_and_places/police_car_light.png',
    'travel_and_places/alarm_clock.png', 'travel_and_places/seven_thirty.png',
    'travel_and_places/ferris_wheel.png',
    'travel_and_places/articulated_lorry.png',
    'travel_and_places/oncoming_bus.png', 'travel_and_places/rollercoaster.png',
    'travel_and_places/snowflake.png', 'travel_and_places/tent.png',
    'travel_and_places/waning_crescent_moon.png',
    'travel_and_places/locomotive.png', 'travel_and_places/airplane.png',
    'travel_and_places/speedboat.png', 'travel_and_places/mountain_cableway.png',
    'travel_and_places/new_moon.png', 'travel_and_places/cloud.png',
    'travel_and_places/volcano.png', 'travel_and_places/eleven_thirty.png',
    'travel_and_places/umbrella_with_rain_drops.png',
    'travel_and_places/train.png', 'travel_and_places/delivery_truck.png',
    'travel_and_places/ten_thirty.png', 'travel_and_places/nine_oclock.png',
    'travel_and_places/hospital.png', 'travel_and_places/classical_building.png',
    'travel_and_places/vertical_traffic_light.png',
    'travel_and_places/ten_oclock.png',
    'travel_and_places/horizontal_traffic_light.png',
    'smileys/face_with_open_mouth.png', 'smileys/sleepy_face.png',
    'smileys/love_letter.png', 'smileys/smiling_face_with_smiling_eyes.png',
    'smileys/pouting_cat.png', 'smileys/persevering_face.png',
    'smileys/winking_face_with_tongue.png', 'smileys/astonished_face.png',
    'smileys/face_with_tears_of_joy.png', 'smileys/tired_face.png',
    'smileys/confused_face.png', 'smileys/ghost.png',
    'smileys/face_without_mouth.png', 'smileys/sad_but_relieved_face.png',
    'smileys/growing_heart.png', 'smileys/hear_no_evil_monkey.png',
    'smileys/kissing_face_with_smiling_eyes.png', 'smileys/pensive_face.png',
    'smileys/fearful_face.png', 'smileys/skull.png', 'smileys/two_hearts.png',
    'smileys/smiling_cat_with_heart_eyes.png',
    'smileys/frowning_face_with_open_mouth.png', 'smileys/smiling_face.png',
    'smileys/crying_cat.png', 'smileys/angry_face.png', 'smileys/ogre.png',
    'smileys/expressionless_face.png', 'smileys/alien_monster.png',
    'smileys/yellow_heart.png', 'smileys/green_heart.png',
    'smileys/speak_no_evil_monkey.png', 'smileys/purple_heart.png',
    'smileys/confounded_face.png', 'smileys/dizzy_face.png',
    'smileys/grinning_face_with_smiling_eyes.png',
    'smileys/loudly_crying_face.png', 'smileys/sleeping_face.png',
    'smileys/beaming_face_with_smiling_eyes.png',
    'smileys/smiling_face_with_sunglasses.png',
    'smileys/grinning_face_with_sweat.png',
    'smileys/grinning_cat_with_smiling_eyes.png',
    'smileys/see_no_evil_monkey.png', 'smileys/red_heart.png',
    'smileys/disappointed_face.png', 'smileys/smiling_face_with_halo.png',
    'smileys/winking_face.png', 'smileys/kissing_cat.png',
    'smileys/grimacing_face.png', 'smileys/goblin.png', 'smileys/alien.png',
    'smileys/grinning_face.png', 'smileys/flushed_face.png',
    'smileys/heart_with_ribbon.png', 'smileys/relieved_face.png',
    'smileys/angry_face_with_horns.png', 'smileys/worried_face.png',
    'smileys/face_with_steam_from_nose.png',
    'smileys/smiling_face_with_horns.png', 'smileys/anxious_face_with_sweat.png',
    'smileys/weary_cat.png', 'smileys/grinning_face_with_big_eyes.png',
    'smileys/face_with_medical_mask.png',
    'smileys/squinting_face_with_tongue.png',
    'smileys/smiling_face_with_heart_eyes.png',
    'smileys/kissing_face_with_closed_eyes.png',
    'smileys/downcast_face_with_sweat.png', 'smileys/cat_with_tears_of_joy.png',
    'smileys/smirking_face.png', 'smileys/hushed_face.png',
    'smileys/crying_face.png', 'smileys/kissing_face.png',
    'smileys/weary_face.png', 'smileys/face_savoring_food.png',
    'smileys/cat_with_wry_smile.png', 'smileys/unamused_face.png',
    'smileys/sparkling_heart.png', 'smileys/pouting_face.png',
    'smileys/grinning_cat.png', 'smileys/anguished_face.png',
    'smileys/neutral_face.png', 'smileys/face_blowing_a_kiss.png',
    'smileys/blue_heart.png', 'smileys/heart_with_arrow.png',
    'smileys/face_with_tongue.png', 'smileys/face_screaming_in_fear.png',
    'smileys/beating_heart.png', 'smileys/revolving_hearts.png',
    'smileys/broken_heart.png', 'smileys/grinning_squinting_face.png',
    'smileys/heart_decoration.png', 'smileys/kiss_mark.png',
    'flags/germany.png', 'flags/spain.png', 'flags/china.png',
    'flags/south_korea.png', 'flags/italy.png', 'flags/united_kingdom.png',
    'flags/russia.png', 'flags/crossed_flags.png', 'flags/japan.png',
    'flags/france.png', 'flags/chequered_flag.png', 'flags/united_states.png',
    'flags/triangular_flag.png', 'objects/pill.png',
    'objects/bell_with_slash.png', 'objects/clutch_bag.png',
    'objects/kimono.png', 'objects/notebook_with_decorative_cover.png',
    'objects/bell.png', 'objects/blue_book.png', 'objects/red_paper_lantern.png',
    'objects/locked_with_pen.png', 'objects/package.png',
    'objects/movie_camera.png', 'objects/mobile_phone_with_arrow.png',
    'objects/black_nib.png', 'objects/envelope_with_arrow.png',
    'objects/round_pushpin.png', 'objects/camera.png', 'objects/newspaper.png',
    'objects/bomb.png', 'objects/floppy_disk.png', 'objects/graduation_cap.png',
    'objects/bookmark.png', 'objects/inbox_tray.png', 'objects/necktie.png',
    'objects/clipboard.png', 'objects/triangular_ruler.png',
    'objects/gem_stone.png', 'objects/mobile_phone.png', 'objects/purse.png',
    'objects/incoming_envelope.png', 'objects/locked.png', 'objects/syringe.png',
    'objects/link.png', 'objects/womans_boot.png', 'objects/microscope.png',
    'objects/video_camera.png', 'objects/telescope.png',
    'objects/chart_increasing.png', 'objects/bikini.png',
    'objects/dollar_banknote.png', 'objects/credit_card.png',
    'objects/card_index.png', 'objects/open_book.png', 'objects/glasses.png',
    'objects/chart_decreasing.png', 'objects/pushpin.png', 'objects/toilet.png',
    'objects/unlocked.png', 'objects/desktop_computer.png', 'objects/scroll.png',
    'objects/ring.png', 'objects/magnifying_glass_tilted_left.png',
    'objects/t_shirt.png', 'objects/telephone.png', 'objects/pencil.png',
    'objects/cigarette.png', 'objects/womans_hat.png', 'objects/postbox.png',
    'objects/paperclip.png', 'objects/lipstick.png', 'objects/flashlight.png',
    'objects/straight_ruler.png', 'objects/telephone_receiver.png',
    'objects/jeans.png', 'objects/fax.png', 'objects/euro_banknote.png',
    'objects/computer_disk.png', 'objects/satellite_antenna.png',
    'objects/high_heeled_shoe.png', 'objects/door.png',
    'objects/videocassette.png', 'objects/moai.png', 'objects/outbox_tray.png',
    'objects/hammer.png', 'objects/electric_plug.png', 'objects/crown.png',
    'objects/yen_banknote.png', 'objects/radio.png',
    'objects/closed_mailbox_with_lowered_flag.png', 'objects/closed_book.png',
    'objects/dress.png', 'objects/bar_chart.png', 'objects/shower.png',
    'objects/battery.png', 'objects/calendar.png', 'objects/bathtub.png',
    'objects/running_shoe.png', 'objects/money_bag.png',
    'objects/nut_and_bolt.png', 'objects/speaker_high_volume.png',
    'objects/television.png', 'objects/handbag.png',
    'objects/womans_sandal.png', 'objects/orange_book.png',
    'objects/money_with_wings.png', 'objects/key.png', 'objects/ledger.png',
    'objects/speaker_low_volume.png', 'objects/light_bulb.png',
    'objects/bookmark_tabs.png', 'objects/speaker_medium_volume.png',
    'objects/pager.png', 'objects/backpack.png', 'objects/locked_with_key.png',
    'objects/page_facing_up.png', 'objects/mans_shoe.png',
    'objects/magnifying_glass_tilted_right.png', 'objects/tear_off_calendar.png',
    'objects/books.png', 'objects/green_book.png', 'objects/pistol.png',
    'objects/womans_clothes.png', 'objects/e_mail.png', 'objects/memo.png',
    'objects/dvd.png', 'objects/postal_horn.png',
    'objects/open_mailbox_with_raised_flag.png', 'objects/notebook.png',
    'objects/closed_mailbox_with_raised_flag.png',
    'objects/open_mailbox_with_lowered_flag.png', 'objects/file_folder.png',
    'objects/pound_banknote.png', 'objects/muted_speaker.png',
    'objects/envelope.png', 'objects/open_file_folder.png',
    'objects/wrench.png', 'objects/page_with_curl.png', 'objects/scissors.png',
    'objects/optical_disk.png', 'alphanumeric/w.png', 'alphanumeric/m.png',
    'alphanumeric/v.png', 'alphanumeric/j.png', 'alphanumeric/q.png',
    'alphanumeric/x.png', 'alphanumeric/h.png', 'alphanumeric/f.png',
    'alphanumeric/d.png', 'alphanumeric/z.png', 'alphanumeric/0.png',
    'alphanumeric/1.png', 'alphanumeric/9.png', 'alphanumeric/6.png',
    'alphanumeric/g.png', 'alphanumeric/e.png', 'alphanumeric/i.png',
    'alphanumeric/5.png', 'alphanumeric/u.png', 'alphanumeric/t.png',
    'alphanumeric/l.png', 'alphanumeric/b.png', 'alphanumeric/s.png',
    'alphanumeric/k.png', 'alphanumeric/3.png', 'alphanumeric/a.png',
    'alphanumeric/2.png', 'alphanumeric/4.png', 'alphanumeric/r.png',
    'alphanumeric/7.png', 'alphanumeric/p.png', 'alphanumeric/o.png',
    'alphanumeric/c.png', 'alphanumeric/n.png', 'alphanumeric/y.png',
    'alphanumeric/8.png'
]
