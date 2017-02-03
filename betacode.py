# Shamelessly stolen from https://github.com/ninjaaron/betacode/blob/master/betacode/hebrew.py

from __future__ import unicode_literals

beta = u')bgdhwzx+yklmns(pcqr#&$t'
hebr = u'אבגדהוזחטיכלמנסעפצקרששׂשׁת'
sub_d = dict(zip(beta, hebr))
# beta_vow = u'a f i e " o u w. : ow :a :f :e - .'.split()
# hebr_vow = u'םַ םָ םִ םֶ םֵ םֹ םֻ וּ  םְ וֹ  םֲ  םֳ  םֱ  ־ םּ'.replace(u'ם', u'').split()
# sub_d.update(dict(zip(beta_vow, hebr_vow)))
beta_vow = u'a f i e " o u w. : ow :a :f :e - .'.split()
hebr_vow = ['','','','','','','','','','','','','','','']
sub_d.update(dict(zip(beta_vow, hebr_vow)))

# beta_accents = "00 01 02 03 04 05 10 13 11 14 24 33 44 60 61 62 63 64 65 80 81 82 83 84 85 35 70 71 72 73 74 75 91 92 93 94 95".split()
# hebr_accents = // see end of file
# sub_d.update(dict(zip(beta_accents, hebr_accents)))

pass_through = set(' \t\n־')

medial = 'כמנפצ'
final  = 'ךםןףץ'
final_d = dict(zip(medial, final))
medial_s = set(medial)


def _finalize(decoded):
    if decoded == []:
        return
    if decoded[-1] in medial_s:
        decoded[-1] = final_d[decoded[-1]]

def decode(betacode):
    betacode = betacode.lower()
    decoded = []
    for char in betacode:
        try:
            decoded.append(sub_d[char])
        except KeyError:
            if char in pass_through:
                _finalize(decoded)
                decoded.append(char)
            elif char !='\\':
                raise
    decoded = list(filter(None, decoded))
    _finalize(decoded)
    return ''.join(decoded)



# "׃" ; --- sop pasuq [end of verse]               -           -
# "֒" .:--- segolta
# "֘"  )--- zarqa, sinnor
# "֙"  \--- pashta, azla legarmeh
# "֩"  &--- telisha parvum
# "׀"  |--- paseq [separator]
# "֚"   ---< yetib (yetiv)
# "13"   ---\ dehi or tipha
# "11"   ---/ (81 + ) mugrash
# "14"   ---% telisha magnum
# "24"  -&-- telisha qetannah (med)
# "33"  --\- pashta (preceding 03)
# "44"  -%-- telisha magnum (med)
# "60"  --<- ole or mahpakatum
# "61"  -/-- geresh or teres
# "62"  -"-- garshajim
# "63"  -\-- azla, azla or qadma
# "64"  -,-- illuj
# "65"  -#-- shalshelet (magn,parv)
# "80"  -:-- zaqep parvum
# "81"  -.-- rebia (magnum=parvum)
# "82"  --)- sinnorit
# "83"  -+-- pazer
# "84" -&%-- pazer mag. or qarne para
# "85" -|:-- zaqep magnum
# "35" -F|:-- meteg (med)
# "70"  -<-- mahpak or mehuppak    I.
# "71"  -/-- mereka
# "72" -//-- mereka kepulah (duplex)
# "73"  -\-- tipha, tarha
# "74"  -,-- munah                 I.
# "75"  -|-- silluq [meteg (left)]
# "91" -./-- tebir
# "92"  -^-- atnah
# "93"  -v-- galgal or jerah
# "94"  -s-- darga
# "95"  -|-- meteg (right) [cf 35,75]
