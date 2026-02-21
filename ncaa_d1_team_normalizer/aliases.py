"""Hardcoded team name aliases for common variants."""

# Keys are lowercase cleaned names (stripped of punctuation), values are ESPN canonical names
TEAM_ALIASES = {
    # -------------------------------------------------------------------------
    # Major Conference Disambiguations & Acronyms
    # -------------------------------------------------------------------------
    # UConn/Connecticut edge case
    'uconn': 'Connecticut',

    # UMass
    'umass': 'Massachusetts',

    # Ole Miss
    'ole miss': 'Mississippi',
    'olemiss': 'Mississippi',

    # Penn vs Penn State disambiguation
    'penn': 'Pennsylvania',
    'penn state': 'Penn State',
    'psu': 'Penn State',

    # Miami disambiguation
    'miami fl': 'Miami (FL)',
    'miami oh': 'Miami (OH)',
    'miami florida': 'Miami (FL)',
    'miami ohio': 'Miami (OH)',
    'the u': 'Miami (FL)',

    # State abbreviations - UNC
    'unc': 'North Carolina',
    'nc state': 'NC State',
    'ncsu': 'NC State',
    'nc st': 'NC State',

    # Common nicknames / Shortnames
    'nova': 'Villanova',
    'cuse': 'Syracuse',
    'ku': 'Kansas',
    'uk': 'Kentucky',
    'bama': 'Alabama',
    'cincy': 'Cincinnati',
    'mizzou': 'Missouri',
    'wazzu': 'Washington State',
    'gt': 'Georgia Tech',
    'cu': 'Colorado',
    'colo': 'Colorado',
    'ksu': 'Kansas State',
    'k state': 'Kansas State',
    'ttu': 'Texas Tech',
    'umd': 'Maryland',
    'rutg': 'Rutgers',
    'illini': 'Illinois',

    # Texas A&M variants
    'texas a m': 'Texas A&M',
    'texas am': 'Texas A&M',
    'texas a and m': 'Texas A&M',
    'tamu': 'Texas A&M',

    # Michigan State variants
    'mich st': 'Michigan State',
    'mich state': 'Michigan State',
    'michigan st': 'Michigan State',
    'msu': 'Michigan State',

    # USC variants
    'southern california': 'USC',
    'southern cal': 'USC',

    # LSU
    'louisiana state': 'LSU',

    # BYU
    'brigham young': 'BYU',

    # SMU
    'southern methodist': 'SMU',

    # TCU
    'texas christian': 'TCU',

    # Pitt
    'pitt': 'Pittsburgh',

    # Cal
    'cal': 'California',
    'california berkeley': 'California',
    'uc berkeley': 'California',

    # VT
    'va tech': 'Virginia Tech',
    'vt': 'Virginia Tech',

    # WVU
    'west virginia': 'West Virginia',
    'wvu': 'West Virginia',

    # OSU
    'ohio state': 'Ohio State',
    'osu': 'Ohio State',

    # ASU
    'arizona state': 'Arizona State',
    'asu': 'Arizona State',

    # FSU
    'florida state': 'Florida State',
    'fsu': 'Florida State',

    # WSU variants (Washington State)
    'washington state': 'Washington State',
    'wsu': 'Washington State',

    # GW
    'george washington': 'George Washington',
    'gw': 'George Washington',


    # -------------------------------------------------------------------------
    # St. / Saint Disambiguations
    # -------------------------------------------------------------------------
    # St. John's
    'st johns': "St. John's (NY)",
    'saint johns': "St. John's (NY)",
    'st johns ny': "St. John's (NY)",
    'sju': "St. John's (NY)",

    # Saint Mary's
    'st marys': "Saint Mary's (CA)",
    'saint marys': "Saint Mary's (CA)",
    'st marys ca': "Saint Mary's (CA)",
    'smc': "Saint Mary's (CA)",

    # SLU
    'st louis': 'Saint Louis',
    'saint louis': 'Saint Louis',
    'slu': 'Saint Louis',

    # SJU (different from St. John's)
    'st josephs': "Saint Joseph's",
    'saint josephs': "Saint Joseph's",
    'st josephs pa': "Saint Joseph's",

    # St. Bonaventure
    'st bonaventure': 'St. Bonaventure',
    'saint bonaventure': 'St. Bonaventure',
    'st bonnies': 'St. Bonaventure',

    # Saint Peter's
    'st peters': "Saint Peter's",
    'saint peters': "Saint Peter's",

    # St. Thomas (MN)
    'st thomas': 'St. Thomas (MN)',
    'saint thomas': 'St. Thomas (MN)',
    'st thomas mn': 'St. Thomas (MN)',


    # -------------------------------------------------------------------------
    # Loyola Disambiguations
    # -------------------------------------------------------------------------
    'loyola': 'Loyola Chicago',
    'loyola chi': 'Loyola Chicago',
    'loyola il': 'Loyola Chicago',
    'loyola md': 'Loyola Maryland',
    'loyola marymount': 'Loyola Marymount',
    'lmu': 'Loyola Marymount',


    # -------------------------------------------------------------------------
    # University of California (UC) & Cal State (CSU) Systems
    # -------------------------------------------------------------------------
    'ucla': 'UCLA',

    'uc santa barbara': 'UC Santa Barbara',
    'ucsb': 'UC Santa Barbara',

    'uc irvine': 'UC Irvine',
    'uci': 'UC Irvine',

    'uc davis': 'UC Davis',
    'ucd': 'UC Davis',

    'uc riverside': 'UC Riverside',
    'ucr': 'UC Riverside',

    'uc san diego': 'UC San Diego',
    'ucsd': 'UC San Diego',

    'cal state fullerton': 'Cal State Fullerton',
    'csuf': 'Cal State Fullerton',

    'cal state bakersfield': 'Cal State Bakersfield',
    'csub': 'Cal State Bakersfield',
    'bakersfield': 'Cal State Bakersfield',

    'cal state northridge': 'CSUN',
    'csun': 'CSUN',
    'northridge': 'CSUN',

    'san diego st': 'San Diego State',
    'san jose st': 'San Jose State',
    'sjsu': 'San Jose State',


    # -------------------------------------------------------------------------
    # Mid-Major Acronyms & Florida Schools
    # -------------------------------------------------------------------------
    'virginia commonwealth': 'VCU',
    'central florida': 'UCF',
    'nevada las vegas': 'UNLV',
    'florida international': 'FIU',
    'fiu': 'FIU',
    'florida atlantic': 'FAU',
    'fau': 'FAU',
    'florida gulf coast': 'FGCU',
    'fla gulf coast': 'FGCU',
    'fgcu': 'FGCU',
    'south florida': 'South Florida',
    'usf': 'South Florida',


    # -------------------------------------------------------------------------
    # Other System Schools (UNC, UT, Texas A&M)
    # -------------------------------------------------------------------------
    'unc wilmington': 'UNCW',
    'uncw': 'UNCW',
    'unc greensboro': 'UNCG',
    'uncg': 'UNCG',
    'unc asheville': 'UNC Asheville',
    'unca': 'UNC Asheville',

    'texas el paso': 'UTEP',
    'texas san antonio': 'UTSA',
    'ut arlington': 'UT Arlington',
    'uta': 'UT Arlington',

    'ut rio grande valley': 'UTRGV',
    'texas pan american': 'UTRGV',
    'utrgv': 'UTRGV',

    'texas a m cc': 'Texas A&M-Corpus Christi',
    'texas am cc': 'Texas A&M-Corpus Christi',
    'tamucc': 'Texas A&M-Corpus Christi',
    'texas a m corpus christi': 'Texas A&M-Corpus Christi',

    'alabama birmingham': 'UAB',
    'illinois chicago': 'UIC',


    # -------------------------------------------------------------------------
    # Recent D1 Name Changes / Institutional Rebrands
    # -------------------------------------------------------------------------
    # IUPUI is now IU Indianapolis (Updated 2024-25 season)
    'iupui': 'IU Indianapolis',
    'indiana purdue indianapolis': 'IU Indianapolis',
    'iu indy': 'IU Indianapolis',

    # Dixie State is now Utah Tech
    'dixie state': 'Utah Tech',

    # IPFW -> Fort Wayne -> Purdue Fort Wayne
    'ipfw': 'Purdue Fort Wayne',
    'fort wayne': 'Purdue Fort Wayne',

    # Little Rock (dropped UALR / Arkansas-)
    'ualr': 'Little Rock',
    'arkansas little rock': 'Little Rock',
    'ark little rock': 'Little Rock',

    # Omaha (dropped Nebraska-)
    'nebraska omaha': 'Omaha',
    'uno': 'Omaha',

    # Long Island University (merged Brooklyn and Post)
    'liu brooklyn': 'LIU',
    'long island university': 'LIU',
    'long island': 'LIU',

    # UMass Lowell
    'mass lowell': 'UMass Lowell',
    'uml': 'UMass Lowell',

    # UAlbany
    'suny albany': 'UAlbany',
    'albany': 'UAlbany',


    # -------------------------------------------------------------------------
    # Directional / State Variants & Miscellaneous
    # -------------------------------------------------------------------------
    # Louisiana Schools
    'louisiana lafayette': 'Louisiana',
    'ul lafayette': 'Louisiana',
    'ull': 'Louisiana',
    'louisiana monroe': 'ULM',
    'ul monroe': 'ULM',
    'ulm': 'ULM',

    # Michigan / Illinois Directionals
    'western mich': 'Western Michigan',
    'wmu': 'Western Michigan',
    'central mich': 'Central Michigan',
    'cmu': 'Central Michigan',
    'eastern mich': 'Eastern Michigan',
    'emu': 'Eastern Michigan',
    'northern ill': 'Northern Illinois',
    'niu': 'Northern Illinois',
    'southern ill': 'Southern Illinois',
    'siu': 'Southern Illinois',
    'southern illinois edwardsville': 'SIU Edwardsville',
    'siue': 'SIU Edwardsville',

    # Wisconsin / Missouri
    'wisconsin green bay': 'Green Bay',
    'uwgb': 'Green Bay',
    'wisconsin milwaukee': 'Milwaukee',
    'uwm': 'Milwaukee',
    'missouri kansas city': 'Kansas City',
    'umkc': 'Kansas City',

    # Common Mid-Majors
    'col of charleston': 'College of Charleston',
    'charleston': 'College of Charleston',
    'cofc': 'College of Charleston',

    'stephen f austin': 'Stephen F. Austin',
    'sfa': 'Stephen F. Austin',

    'detroit': 'Detroit Mercy',
    'udm': 'Detroit Mercy',

    'bowling green': 'Bowling Green',
    'bgsu': 'Bowling Green',

    'middle tenn': 'Middle Tennessee',
    'mtsu': 'Middle Tennessee',

    'east tennessee state': 'ETSU',
    'southern miss': 'Southern Miss',
    'usm': 'Southern Miss',

    'north carolina a t': 'North Carolina A&T',
    'nc a t': 'North Carolina A&T',
    'ncat': 'North Carolina A&T',

    'north carolina central': 'North Carolina Central',
    'nccu': 'North Carolina Central',
}
