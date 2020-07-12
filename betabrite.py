#!/usr/bin/env python3

import time
import serial

################################################################################

#### Frame Control Bytes

WAKEUP = b"\x00\x00\x00\x00\x00\x00";	# Wakes up the sign and
										#   negotiates communication
										#   speed

SIGN_ADDRESS_BROADCAST = b"00"			# can be anything between "00" and "FF"
										#   hexcode, 00 is broadcast
										#   Can be wildcarded with ? (e.g. "0?"
										#   addresses "01" - "0F")
SIGN_TYPE_ALL_VERIFY        = b"!";	# all signs
									#   Verify success by displaying
									#   "TRANSMISSION OK" or
									#   "TRANSMISSION ERROR"
SIGN_TYPE_SERIAL_CLOCK      = b"\"";	# serial clock
SIGN_TYPE_ALPHAVISION       = b"#";	# alphavision
SIGN_TYPE_ALPHAVISION_FULL  = b"$";	# full matrix alphavision
SIGN_TYPE_ALPHAVISION_CHAR  = b"%";	# character matrix alphavision
SIGN_TYPE_ALPHAVISION_LINE  = b"&";	# line matrix alphavision
SIGN_TYPE_RESPONSE          = b"0";	# sign response
SIGN_TYPE_ONE_LINE          = b"1";	# one line signs
SIGN_TYPE_TWO_LINE          = b"2";	# two line signs
SIGN_TYPE_ALL               = b"?";	# all signs (except BetaBrite)
SIGN_TYPE_430I              = b"C";	# 430i
SIGN_TYPE_440I              = b"D";	# 440i
SIGN_TYPE_460I              = b"E";	# 460i
SIGN_TYPE_790I              = b"U";	# 790i
SIGN_TYPE_ALL               = b"Z";	# all signs
SIGN_TYPE_BETABRITE         = b"^";	# betabrite
SIGN_TYPE_4120C             = b"a";	# 4120c
SIGN_TYPE_4160C             = b"b";	# 4160c
SIGN_TYPE_4200C             = b"c";	# 4200c
SIGN_TYPE_4240C             = b"d";	# 4240c
SIGN_TYPE_215               = b"e";	# 215
SIGN_TYPE_215C              = b"f";	# 215c
SIGN_TYPE_4120R             = b"g";	# 4120r
SIGN_TYPE_4160R             = b"h";	# 4160r
SIGN_TYPE_4200R             = b"i";	# 4200r
SIGN_TYPE_4240R             = b"j";	# 4240r
SIGN_TYPE_300               = b"k";	# 300
SIGN_TYPE_7000              = b"l";	# 7000
SIGN_TYPE_SOLAR_96X16       = b"m";	# solar 96x16 matrix
SIGN_TYPE_SOLAR_128X16      = b"n";	# solar 128x16 matrix
SIGN_TYPE_SOLAR_160X16      = b"o";	# solar 160x16 matrix
SIGN_TYPE_SOLAR_192X16      = b"p";	# solar 192x16 matrix
SIGN_TYPE_SOLAR_PPD         = b"q";	# ppd
SIGN_TYPE_DIRECTOR          = b"r";	# director
SIGN_TYPE_4080C             = b"t";	# 4080c
SIGN_TYPE_2X0C              = b"u";	# 210c and 220c
SIGN_TYPE_ALL_CONFIG        = b"z";	# all signs
                                    #   configure memory for 26 files (A-Z)
                                    #   of 150 characters each, then
	                                #   execute the command
COMMAND_WRITE_TEXT       = b"A";	# write TEXT file
COMMAND_READ_TEXT        = b"B";	# read TEXT file
COMMAND_WRITE_SPECIAL    = b"E";	# write SPECIAL function
COMMAND_READ_SPECIAL     = b"F";	# read SPECIAL function
COMMAND_WRITE_STRING     = b"G";	# write STRING file
COMMAND_READ_STRING      = b"H";	# read STRING file
COMMAND_WRITE_DOTS       = b"I";	# write DOTS picture
COMMAND_READ_DOTS        = b"J";	# read DOTS picture
COMMAND_WRITE_ALPHA_DOTS = b"M";	# write ALPHAVISION DOTS picture
COMMAND_READ_ALPHA_DOTS  = b"N";	# read ALPHAVISION DOTS picture
COMMAND_ALPHA_BULLETIN   = b"O";	# write ALPHAVISION BULLETIN

FILE_PRIORITY = b"0"                # Can be anything in 0x20 to 0x7E
                                    #   Note: 0x30 ("0") is reserved for priorty
                                    #   TEXT messages, and "0" and "?" (0x3F)
                                    #   can not be used to store STRINGS

PRINT2_SOH = b"]\!";			    # 2 byte printable SOH
PRINT2_STX = b"]\"";		        # 2 byte printable STX
PRINT2_EOT = b"]$"; 		        # 2 byte printable EOT

PRINT3_SOH = b"_01";			    # 3 byte printable SOH
PRINT3_STX = b"_02";			    # 3 byte printable STX
PRINT3_EOT = b"_04";			    # 3 byte printable EOT

CMD_WRITE_TEXT = b"A";			# write TEXT file
CMD_READ_TEXT  = b"B";			# read TEXT file


TEXT_POS_MIDDLE = b" ";			# center text vertically
TEXT_POS_TOP    = b"\"";		# text begins at top and at most n-1
					#   lines
TEXT_POS_BOTTOM = b"&";			# text immediatly follows the TOP
TEXT_POS_FILL   = b"0";			# center text verically and use all
					#   available lines

MODE_ROTATE      = b"a";		# rotate right to left
MODE_HOLD        = b"b";		# stationary
MODE_FLASH       = b"c";		# stationary and flash
MODE_ROLLUP      = b"e";		# push up old message by new message
MODE_ROLLDOWN    = b"f";		# push down old message by new message
MODE_ROLLLEFT    = b"g";		# push left old message by new message
MODE_ROLLRIGHT   = b"h";		# push right old message by new message
MODE_WIPEUP      = b"i";		# wipe up over old message with new
MODE_WIPEDOWN    = b"j";		# wipe down over old message with new
MODE_WIPELEFT    = b"k";		# wipe left over old message with new
MODE_WIPERIGHT   = b"l";		# wipe right over old message with new
MODE_SCROLL      = b"m";		# new message pushes the bottom line
					#   to the top of a 2 line sign
MODE_AUTO        = b"o";		# random mode selected automatically
MODE_ROLLIN      = b"p";		# new message pushed inward
MODE_ROLLOUT     = b"q";		# new message pushed outward
MODE_WIPEIN      = b"r";		# new message wiped over old inward
MODE_WIPEOUT     = b"s";		# new message wiped over old outward
MODE_CMPRSROT    = b"t";		# rotate right to left with text
					#   only half as wide
MODE_TWINKLE     = b"n0";		# twinkle message
MODE_SPARKLE     = b"n1";		# new message sparkles over the old
MODE_SNOW        = b"n2";		# snow the new message
MODE_INTERLOCK   = b"n3";		# new message interlocks over the old
MODE_SWITCH      = b"n4";		# switch "off" the old message char by
					#   char.  new message switches "on"
					#   char by char
MODE_SLIDE       = b"n5";		# slide chars right to left one at a
					#   time
MODE_SPRAY       = b"n6";		# spray message right to left
MODE_STARBURST   = b"n7";		# explode new message
MODE_WELCOME     = b"n8";		# display a script "Welcome"
MODE_SLOTMACHINE = b"n9";		# display slot machine reels
MODE_NEWSFLASH   = b"nA";		# display "Newsflash" animation
MODE_TRUMPET     = b"nB";		# display a trumpet animation
MODE_THANKYOU    = b"nS";		# display a script "Thank You"
MODE_NOSMOKING   = b"nU";		# display "No Smoking" animationl
MODE_DRINKDRIVE  = b"nV";		# display "Don't Drink and Drive"
					#   animation
MODE_ANIMAL      = b"nW";		# display a running animal
MODE_FISH        = b"nW";		# display fish
					#   (BetaBrite alternate for ANIMAL)
MODE_FIREWORKS   = b"nX";		# display fireworks animation
MODE_TURBOCAR    = b"nY";		# display a car animation
MODE_BALLOONS    = b"nY";		# display a balloon animation
					#   (BetaBrite alternate for TURBOCAR)
MODE_CHERRYBOMB  = b"nZ";		# display a cherry bomb animation



BULLETIN_POS_TOP    = b"T";		# display bulletin at the top
BULLETIN_POS_BOTTOM = b"B";		# display bulletin at the bottom

BULLETIN_JUST_LEFT   = b"L";		# left justify bulletin
BULLETIN_JUST_RIGHT  = b"R";		# right justify bulletin
BULLETIN_JUST_CENTER = b"C";		# center bulletin



#### character table

NUL                  = b"\x00";		# NULl
SOH                  = b"\x01";		# Start Of Header
STX                  = b"\x02";		# Start Of Text
ETX                  = b"\x03";		# End of TeXt
EOT                  = b"\x04";		# End Of Transmission
DBL_HEIGHT_CHARS_ON  = b"\x05\x30";	# double height chars off (def)
DBL_HEIGHT_CHARS_OFF = b"\x05\x31";	# double height chars on
TRUE_DESCENDERS_ON   = b"\x06\x30";	# true descenders off (default)
TRUE_DESCENDERS_OFF  = b"\x06\x31";	# true descenders on
CHAR_FLASH_ON        = b"\x07\x30";	# character flash off (default)
CHAR_FLASH_OFF       = b"\x07\x31";	# character flash off (default)
TEMP_CELSIUS         = b"\x08\x1c";	# current temperature in celsius
TEMP_FAHRENHEIT      = b"\x08\x1d";	# current temperature in fahrenheit
XC_C_TAIL            = b"\x08\x20";	# capital 'c' with tail
XC_u_UMLAUT          = b"\x08\x21";	# lowercase 'u' with umlaut
XC_e_GRAVE           = b"\x08\x22";	# lowercase 'e' with grave accent
XC_a_CIRCUMFLEX      = b"\x08\x23";	# lowercase 'a' with circumflex
XC_a_UMLAUT          = b"\x08\x24";	# lowercase 'a' with umlaut
XC_a_ACCENT          = b"\x08\x25";	# lowercase 'a' with accent
XC_a_CIRCLE          = b"\x08\x26";	# lowercase 'a' with circle
XC_c_TAIL            = b"\x08\x27";	# lowercase 'c' with tail
XC_e_CIRCUMFLEX      = b"\x08\x28";	# lowercase 'e' with circumflex
XC_e_UMLAUT          = b"\x08\x29";	# lowercase 'e' with umlaut
XC_e_GRAVE           = b"\x08\x2a";	# lowercase 'e' with grave accent
XC_i_UMLAUT          = b"\x08\x2b";	# lowercase 'i' with umlaut
XC_i_CIRCUMFLEX      = b"\x08\x2c";	# lowercase 'i' with circumflex
XC_i_GRAVE           = b"\x08\x2d";	# lowercase 'i' with grave accent
XC_A_UMLAUT          = b"\x08\x2e";	# capital 'a' with umlaut
XC_A_CIRCLE          = b"\x08\x2f";	# capital 'a' with circle
XC_E_ACCENT          = b"\x08\x30";	# capital 'e' with accent
XC_ae_LIGATURE       = b"\x08\x31";	# lowercase 'ae' ligature
XC_AE_LIGATURE       = b"\x08\x32";	# capital 'ae' ligature
XC_o_CIRCUMFLEX      = b"\x08\x33";	# lowercase 'o' with circumflex
XC_o_UMLAUT          = b"\x08\x34";	# lowercase 'o' with umlaut
XC_o_GRAVE           = b"\x08\x35";	# lowercase 'o' with grave accent
XC_u_CIRCUMFLEX      = b"\x08\x36";	# lowercase 'u' with circumflex
XC_u_GRAVE           = b"\x08\x37";	# lowercase 'u' with grave accent
XC_y_UMLAUT          = b"\x08\x38";	# lowercase 'y' with umlaut
XC_O_UMLAUT          = b"\x08\x39";	# capital 'o' with umlaut
XC_U_UMLAUT          = b"\x08\x3a";	# capital 'u' with umlaut
XC_CENTS             = b"\x08\x3b";	# cents sign
XC_POUNDS            = b"\x08\x3c";	# british pounds sign
XC_YEN               = b"\x08\x3d";	# yen sign
XC_PERCENT           = b"\x08\x3e";	# percent sign
XC_SLANT_F           = b"\x08\x3f";	# slant lowercase f
XC_a_ACCENT          = b"\x08\x40";	# lowercase 'a' with accent
XC_i_ACCENT          = b"\x08\x41";	# lowercase 'i' with accent
XC_o_ACCENT          = b"\x08\x42";	# lowercase 'o' with accent
XC_u_ACCENT          = b"\x08\x43";	# lowercase 'u' with accent
XC_n_TILDE           = b"\x08\x44";	# lowercase 'n' with tilde
XC_N_TILDE           = b"\x08\x45";	# capital 'n' with tilde
XC_SUPER_a           = b"\x08\x46";	# superscript 'a'
XC_SUPER_o           = b"\x08\x47";	# superscript 'o'
XC_INVERT_QUESTION   = b"\x08\x48";	# inverted question mark
XC_DEGREES           = b"\x08\x49";	# degree sign (superscript circle)
XC_INVERT_EXCLAIM    = b"\x08\x4a";	# inverted exclaimation mark
XC_SINGLE_COL_SPACE  = b"\x08\x4b";	# single column space
XC_theta             = b"\x08\x4c";	# lowercase theta
XC_THETA             = b"\x08\x4d";	# capital theta
XC_c_ACCENT          = b"\x08\x4e";	# lowercase 'c' with accent
XC_C_ACCENT          = b"\x08\x4f";	# capital 'c' with accent
XC_c                 = b"\x08\x50";	# lowercase 'c'
XC_C                 = b"\x08\x51";	# capital 'c'
XC_d                 = b"\x08\x52";	# lowercase 'd'
XC_D                 = b"\x08\x53";	# capital 'd'
XC_s                 = b"\x08\x54";	# lowercase 's'
XC_z                 = b"\x08\x55";	# lowercase 'z'
XC_Z                 = b"\x08\x56";	# capital 'z'
XC_BETA              = b"\x08\x57";	# beta
XC_S                 = b"\x08\x58";	# capital 's'
XC_BETA2             = b"\x08\x59";	# beta
XC_A_ACCENT          = b"\x08\x5a";	# capital 'a' with accent
XC_A_GRAVE           = b"\x08\x5b";	# capital 'a' with grave accent
XC_A_2ACCENT         = b"\x08\x5c";	# capital 'a' with two accents
XC_a_2ACCENT         = b"\x08\x5d";	# lowercase ''a' with two accents
XC_E_ACCENT          = b"\x08\x5e";	# capital 'e' with accent
XC_I_ACCENT          = b"\x08\x5f";	# capital 'i' with accent
XC_O_TILDE           = b"\x08\x60";	# capital 'o' with tilde
XC_o_TILDE           = b"\x08\x61";	# lowecase 'o' with tilde
COUNTER_1            = b"\x08\x7a";	# current value in counter 1
COUNTER_2            = b"\x08\x7b";	# current value in counter 2
COUNTER_3            = b"\x08\x7c";	# current value in counter 3
COUNTER_4            = b"\x08\x7d";	# current value in counter 4
COUNTER_5            = b"\x08\x7e";	# current value in counter 4
NO_HOLD_SPEED        = b"\x09";		# no hold speed  (no pause following
					#   the mode presentation.  not
					#   applicable to ROTATE or
					#   COMPRESSED_ROTATE modes)
LF                   = b"\x0a";		# Line Feed
CURDATE_MMDDYY_SLASH = b"\x0b\x30";	# current date MM/DD/YY
CURDATE_DDMMYY_SLASH = b"\x0b\x31";	# current date DD/MM/YY
CURDATE_MMDDYY_DASH  = b"\x0b\x32";	# current date MM-DD-YY
CURDATE_DDMMYY_DASH  = b"\x0b\x33";	# current date DD-MM-YY
CURDATE_MMDDYY_DOT   = b"\x0b\x34";	# current date MM.DD.YY
CURDATE_DDMMYY_DOT   = b"\x0b\x35";	# current date DD.MM.YY
CURDATE_MMDDYY_SPACE = b"\x0b\x36";	# current date MM DD YY
CURDATE_DDMMYY_SPACE = b"\x0b\x37";	# current date DD MM YY
CURDATE_MMMDDYYYY    = b"\x0b\x38";	# current date MMM.DD, YYYY
CURDATE_WEEKDAYY     = b"\x0b\x39";	# current day of week
NEW_PAGE             = b"\x0c";		# start next display page
CR                   = b"\x0d";		# Carriage Return (new line)
NEWLINE              = CR;
STRING_FILE_INSERT   = b"\x10";		# insert STRING file (next char is
					#   the filename)
WIDE_CHARS_OFF       = b"\x11";		# disable wide characters
WIDE_CHARS_ON        = b"\x12";		# enables wide characters
CURTIME_INSERT       = b"\x13";		# current time
DOTS_INSERT          = b"\x14";		# insert DOTS picture (next char is
					#   the filename)
SPEED_1              = b"\x15";		# set scroll speed to 1 (slowest)
SPEED_2              = b"\x16";		# set scroll speed to 2
SPEED_3              = b"\x17";		# set scroll speed to 3
SPEED_4              = b"\x18";		# set scroll speed to 4
SPEED_5              = b"\x19";		# set scroll speed to 5 (fastest)
CHARSET_5_NORMAL     = b"\x1a\x31";	# set character set 5 high normal
CHARSET_7_NORMAL     = b"\x1a\x33";	# set character set 7 high normal
CHARSET_7_FANCY      = b"\x1a\x35";	# set character set 7 high fancy
CHARSET_10_NORMAL    = b"\x1a\x36";	# set character set 10 high normal
CHARSET_FULL_FANCY   = b"\x1a\x38";	# set character set full height fancy
CHARSET_FULL_NORMAL  = b"\x1a\x39";	# set character set full height normal
SOM                  = b"\x1b";		# Start Of Mode
TEXT_COLOR_RED       = b"\x1c\x31";	# set text color to red
TEXT_COLOR_GREEN     = b"\x1c\x32";	# set text color to green
TEXT_COLOR_AMBER     = b"\x1c\x33";	# set text color to amber
TEXT_COLOR_DIMRED    = b"\x1c\x34";	# set text color to dim red
TEXT_COLOR_DIMGREEN  = b"\x1c\x35";	# set text color to dim green
TEXT_COLOR_BROWN     = b"\x1c\x36";	# set text color to brown
TEXT_COLOR_ORANGE    = b"\x1c\x37";	# set text color to orange
TEXT_COLOR_YELLOW    = b"\x1c\x38";	# set text color to yellow
TEXT_COLOR_RAINBOW1  = b"\x1c\x39";	# set text color to rainbow all chars
TEXT_COLOR_RAINBOW2  = b"\x1c\x41";	# set text color to rainbow indiv chars
TEXT_COLOR_MIX       = b"\x1c\x42";	# each char gets a differnt color
TEXT_COLOR_AUTO      = b"\x1c\x43";	# cycle through color modes
CHAR_ATTRIB_WIDE_ON  = b"\x1d\x30\x31";	# char attrib wide on
CHAR_ATTRIB_WIDE_OFF = b"\x1d\x30\x30";	# char attrib wide off
CHAR_ATTRIB_DBLW_ON  = b"\x1d\x31\x31";	# char attrib dbl width on
CHAR_ATTRIB_DBLW_OFF = b"\x1d\x31\x30";	# char attrib dbl width off
CHAR_ATTRIB_DBLH_ON  = b"\x1d\x32\x31";	# char attrib dbl height on
CHAR_ATTRIB_DBLH_OFF = b"\x1d\x32\x30";	# char attrib dbl height off
CHAR_ATTRIB_DESC_ON  = b"\x1d\x33\31";	# char attrib true desc on
CHAR_ATTRIB_DESC_OFF = b"\x1d\x33\30";	# char attrib true desc off
CHAR_ATTRIB_FIX_ON   = b"\x1d\x34\x31";	# char attrib fixed width on
CHAR_ATTRIB_FIX_OFF  = b"\x1d\x34\x30";	# char attrib fixed width off
CHAR_ATTRIB_FNCY_ON  = b"\x1d\x35\x31";	# char attrib fancy on
CHAR_ATTRIB_FNCY_OFF = b"\x1d\x35\x30";	# char attrib fancy off
FIXED_WIDTH_OFF      = b"\x1e\x30";	# fixed width chars off (default)
FIXED_WIDTH_ON       = b"\x1e\x31";	# fixed width chars on
ALPHA_DOTS_INSERT    = b"\x1f";		# insert ALPHAVISION DOTS picture
					#   must be followed by:
					#   SFFFFFFFFFtttt
					#     S = b"C" file is part of a
					#               QuickFlick animation.
					#               Clear display and uses
					#               hold time
					#     S = b"L" file is a DOTS picture.
					#               if inserted in a
					#               TEXT file, then hold
					#               time is ignored
					#     Fx9 = filename (pad with SPACEs)
					#     tttt = 4 digit ascii hexnum
					#              indicating tenths of
					#              of seconds
CENTS                = b"^";		# cents sign
HALF_SPACE           = b"~";		# half a space
BLOCK_CHAR           = b"\x7f";		# a square block character
C_TAIL               = b"\x80";		# capital 'c' with tail
u_UMLAUT             = b"\x81";		# lowercase 'u' with umlaut
e_GRAVE              = b"\x82";		# lowercase 'e' with grave accent
a_CIRCUMFLEX         = b"\x83";		# lowercase 'a' with circumflex
a_UMLAUT             = b"\x84";		# lowercase 'a' with umlaut
a_ACCENT             = b"\x85";		# lowercase 'a' with accent
a_CIRCLE             = b"\x86";		# lowercase 'a' with circle
c_TAIL               = b"\x87";		# lowercase 'c' with tail
e_CIRCUMFLEX         = b"\x88";		# lowercase 'e' with circumflex
e_UMLAUT             = b"\x89";		# lowercase 'e' with umlaut
e_GRAVE              = b"\x8a";		# lowercase 'e' with grave accent
i_UMLAUT             = b"\x8b";		# lowercase 'i' with umlaut
i_CIRCUMFLEX         = b"\x8c";		# lowercase 'i' with circumflex
i_GRAVE              = b"\x8d";		# lowercase 'i' with grave accent
A_UMLAUT             = b"\x8e";		# capital 'a' with umlaut
A_CIRCLE             = b"\x8f";		# capital 'a' with circle
E_ACCENT             = b"\x90";		# capital 'e' with accent
ae_LIGATURE          = b"\x91";		# lowercase 'ae' ligature
AE_LIGATURE          = b"\x92";		# capital 'ae' ligature
o_CIRCUMFLEX         = b"\x93";		# lowercase 'o' with circumflex
o_UMLAUT             = b"\x94";		# lowercase 'o' with umlaut
o_GRAVE              = b"\x95";		# lowercase 'o' with grave accent
u_CIRCUMFLEX         = b"\x96";		# lowercase 'u' with circumflex
u_GRAVE              = b"\x97";		# lowercase 'u' with grave accent
y_UMLAUT             = b"\x98";		# lowercase 'y' with umlaut
O_UMLAUT             = b"\x99";		# capital 'o' with umlaut
U_UMLAUT             = b"\x9a";		# capital 'u' with umlaut
CENTS                = b"\x9b";		# cents sign
POUNDS               = b"\x9c";		# british pounds sign
YEN                  = b"\x9d";		# yen sign
PERCENT              = b"\x9e";		# percent sign
SLANT_F              = b"\x9f";		# slant lowercase f
a_ACCENT             = b"\xa0";		# lowercase 'a' with accent
i_ACCENT             = b"\xa1";		# lowercase 'i' with accent
o_ACCENT             = b"\xa2";		# lowercase 'o' with accent
u_ACCENT             = b"\xa3";		# lowercase 'u' with accent
n_TILDE              = b"\xa4";		# lowercase 'n' with tilde
N_TILDE              = b"\xa5";		# capital 'n' with tilde
SUPER_a              = b"\xa6";		# superscript 'a'
SUPER_o              = b"\xa7";		# superscript 'o'
INVERT_QUESTION      = b"\xa8";		# inverted question mark
DEGREES              = b"\xa9";		# degree sign (superscript circle)
INVERT_EXCLAIM       = b"\xaa";		# inverted exclaimation mark
SINGLE_COL_SPACE     = b"\xab";		# single column space
theta                = b"\xac";		# lowercase theta
THETA                = b"\xad";		# capital theta
c_ACCENT             = b"\xae";		# lowercase 'c' with accent
C_ACCENT             = b"\xaf";		# capital 'c' with accent
CHAR_c               = b"\xb0";		# lowercase 'c'
CHAR_C               = b"\xb1";		# capital 'c'
CHAR_d               = b"\xb2";		# lowercase 'd'
CHAR_D               = b"\xb3";		# capital 'd'
CHAR_s               = b"\xb4";		# lowercase 's'
CHAR_z               = b"\xb5";		# lowercase 'z'
CHAR_Z               = b"\xb6";		# capital 'z'
BETA                 = b"\xb7";		# beta
CHAR_S               = b"\xb8";		# capital 's'
BETA2                = b"\xb9";		# beta
A_ACCENT             = b"\xba";		# capital 'a' with accent
A_GRAVE              = b"\xbb";		# capital 'a' with grave accent
A_2ACCENT            = b"\xbc";		# capital 'a' with two accents
a_2ACCENT            = b"\xbd";		# lowercase ''a' with two accents
E_ACCENT             = b"\xbe";		# capital 'e' with accent
I_ACCENT             = b"\xbf";		# capital 'i' with accent
O_TILDE              = b"\xc0";		# capital 'o' with tilde
o_TILDE              = b"\xc1";		# lowecase 'o' with tilde

################################################################################

def transmit(port, payload, addr=SIGN_ADDRESS_BROADCAST, type=SIGN_TYPE_ALL_VERIFY):
    #packet = WAKEUP + SOM  + MODE_ROTATE + TEXT_COLOR_YELLOW + BETA2 + bytes(msg, 'utf-8') + EOT
    #packet = WAKEUP + SOH + type  + addr + STX + MODE_ROTATE + TEXT_COLOR_YELLOW + BETA2 + bytes(msg, 'utf-8') + EOT
    #packet = b"\x00\x00\x00\x00\x00\x00\x01!00\x02A0\x1b c" + bytes(msg, 'utf-8') + b"\x04"

    packet = WAKEUP + SOH + type + addr + STX + payload + EOT
    ser = serial.Serial(port, 9600, timeout=10)
    ser.write(packet)
    time.sleep(2)
    ser.close()

def write_file(animations, file=FILE_PRIORITY):
    payload = COMMAND_WRITE_TEXT + file
    for animation in animations:
        payload += animation
    return payload

def animation(msg, mode=MODE_AUTO, color=TEXT_COLOR_AUTO, position=TEXT_POS_MIDDLE):
    return  SOM + position + mode + color + transcode(msg)

def soft_reset():
    return COMMAND_WRITE_SPECIAL + b"\x2c"

def transcode(msg):
    b = bytes(msg, 'utf-8')
    b = b.replace(b'\xc2\xb0', DEGREES)
    return b

################################################################################

def parse_cmdline_messages(tokens):
    animations = []
    text = ''
    mode = MODE_AUTO
    color = TEXT_COLOR_AUTO
    position = TEXT_POS_MIDDLE
    for tok in tokens:
        if len(tok) == 0:
            continue

        if tok[0] == '+':
            if text != '':
                animations.append(animation(text, mode, color, position))
                text = ''
                mode = MODE_AUTO
                color = TEXT_COLOR_AUTO
                position = TEXT_POS_MIDDLE
            if tok == '+middle':
                position = TEXT_POS_MIDDLE
            elif tok == '+top':
                position = TEXT_POS_TOP
            elif tok == '+bottom':
                position = TEXT_POS_BOTTOM
            elif tok == '+fill':
                position = TEXT_POS_FILL
            elif tok == '+red':
                color = TEXT_COLOR_RED
            elif tok == '+green':
                color = TEXT_COLOR_GREEN
            elif tok == '+amber':
                color = TEXT_COLOR_AMBER
            elif tok == '+dimred':
                color = TEXT_COLOR_DIMRED
            elif tok == '+brown':
                color = TEXT_COLOR_BROWN
            elif tok == '+orange':
                color = TEXT_COLOR_ORANGE
            elif tok == '+yellow':
                color = TEXT_COLOR_YELLOW
            elif tok == '+rainbow1':
                color = TEXT_COLOR_RAINBOW1
            elif tok == '+rainbow2':
                color = TEXT_COLOR_RAINBOW2
            elif tok == '+mix':
                color = TEXT_COLOR_MIX
            elif tok == '+autocolor':
                color = TEXT_COLOR_AUTO
            elif tok == '+rotate':
                mode = MODE_ROTATE
            elif tok == '+hold':
                mode = MODE_HOLD
            elif tok == '+flash':
                mode = MODE_FLASH
            elif tok == '+rollup':
                mode = MODE_ROLLUP
            elif tok == '+rolldown':
                mode = MODE_ROLLDOWN
            elif tok == '+rollleft':
                mode = MODE_ROLLLEFT
            elif tok == '+rollright':
                mode = MODE_ROLLRIGHT
            elif tok == '+wipeup':
                mode = MODE_WIPEUP
            elif tok == '+wipedown':
                mode = MODE_WIPEDOWN
            elif tok == '+wipeleft':
                mode = MODE_WIPELEFT
            elif tok == '+wiperight':
                mode = MODE_WIPERIGHT
            elif tok == '+scroll':
                mode = MODE_SCOLL
            elif tok == '+automode':
                mode = MODE_AUTO
            elif tok == '+rollin':
                mode = MODE_ROLLIN
            elif tok == '+rollout':
                mode = MODE_ROLLOUT
            elif tok == '+wipein':
                mode = MODE_WIPEIN
            elif tok == '+wipeout':
                mode = MODE_WIPEOUT
            elif tok == '+cmprsrot':
                mode = MODE_CMPRSROT
            elif tok == '+twinkle':
                mode = MODE_TWINKLE
            elif tok == '+sparkle':
                mode = MODE_SPARKLE
            elif tok == '+snow':
                mode = MODE_SNOW
            elif tok == '+interlock':
                mode = MODE_INTERLOCK
            elif tok == '+switch':
                mode = MODE_SWITCH
            elif tok == '+spray':
                mode = MODE_SPRAY
            elif tok == '+starburst':
                mode = MODE_STARBURST
            elif tok == '+welcome':
                mode = MODE_WELCOME
            elif tok == '+slotmachine':
                mode = MODE_SLOTMACHINE
            elif tok == '+newsflash':
                mode = MODE_NEWSFLASH
            elif tok == '+trumpet':
                mode = MODE_TRUMPET
            elif tok == '+thankyou':
                mode = MODE_THANKYOU
            elif tok == '+nosmoking':
                mode = MODE_NOSMOKING
            elif tok == '+drinkdrive':
                mode = MODE_DRINKDRIVE
            elif tok == '+animal':
                mode = MODE_ANIMAL
            elif tok == '+fish':
                mode = MODE_FISH
            elif tok == '+fireworks':
                mode = MODE_FIREWORKS
            elif tok == '+turbocar':
                mode = MODE_TURBOCAR
            elif tok == '+balloons':
                mode = MODE_BALLOONS
            elif tok == '+cherrybomb':
                mode = MODE_CHERRYBOMB
        else:
            if len(text) > 0:
                text += ' '
            text += tok
    animations.append(animation(text, mode, color, position))

    return animations

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", help="Port to write to", default='/dev/cu.usbserial-A4007B5o')
    parser.add_argument("messages", help="Formatted messages to send", nargs='+')
    args = parser.parse_args()

    animations = parse_cmdline_messages(args.messages)

    #animations = [ animation('', MODE_BALLOONS),
    #               animation(sys.argv[1], MODE_SPRAY, TEXT_COLOR_YELLOW),
    #               animation(sys.argv[2], MODE_CMPRSROT, TEXT_COLOR_RED),
    #               animation('', MODE_FISH),
    #               animation('extra', MODE_STARBURST, TEXT_COLOR_RAINBOW1) ]
    transmit(args.port, write_file(animations))
