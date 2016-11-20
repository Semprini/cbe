# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from genericm2m.models import RelatedObjectsDescriptor

class Place(models.Model):
    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)
    
    class Meta:
        abstract = True

        
#class GeographicPlace(Place):
#
#    class Meta:
#        abstract = True


#class LocalPlace(Place):
#
#    class Meta:
#        abstract = True

        
class Country(Place):
    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=200)
    
    iso2_code = models.CharField(max_length=2, blank=True)
    iso_numeric = models.IntegerField(null=True)
    
    #capital
    #population
    #continent
    #currency - new ABE
    #phone
    #postal code format
    #languages
    #neighbours
    #timezones

    def __str__(self):
        return self.name

        
    def country_geo_data(self, filename = None):
        pass


class City(Place):
    country = models.ForeignKey(Country)
    name = models.CharField(max_length=200)


class GeographicAddress(Place):
    country = models.ForeignKey(Country, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True)
    state_or_province = models.CharField(max_length=200, blank=True)

    class Meta:
        abstract = True

        
class UrbanPropertyAddress(GeographicAddress):
    locality = models.CharField(max_length=200, blank=True)
    postcode = models.CharField(max_length=50, blank=True)
    street_name = models.CharField(max_length=200, blank=True)
    street_number_first = models.IntegerField(blank=True, null=True)
    street_number_first_suffix = models.CharField(max_length=20, blank=True)
    street_number_last = models.IntegerField(blank=True, null=True)
    street_number_last_suffix = models.CharField(max_length=20, blank=True)
    street_suffix = models.CharField(max_length=50, blank=True)
    street_type = models.CharField(max_length=100, blank=True)

    def __str__(self):
        ret = ""
        if self.street_number_first is not None:
            ret += "%d%s "%(self.street_number_first, self.street_number_first_suffix)

        if self.street_name != "":
            ret += "%s "%self.street_name
            
        if self.street_type != "":
            ret += "%s"%self.street_type

        if self.locality != "":
            ret += ", %s"%self.locality

        if self.city != "":
            ret += ", %s"%self.city
        
        return  ret
    
    
class UrbanPropertySubAddress(GeographicAddress):
    urban_property_address = models.ForeignKey(UrbanPropertyAddress,)
    building_name = models.CharField(max_length=200, blank=True, null=True)
    level_number = models.CharField(max_length=20, blank=True, null=True)
    level_type = models.CharField(max_length=50, blank=True, null=True)
    private_street_name = models.CharField(max_length=150, blank=True, null=True)
    sub_unit_number = models.CharField(max_length=20, blank=True, null=True)
    sub_unit_type = models.CharField(max_length=100, blank=True, null=True)
    
    
class RuralPropertyAddress(GeographicAddress):
    street_name = models.CharField(max_length=200, blank=True)
    postcode = models.CharField(max_length=50, blank=True)
    locality = models.CharField(max_length=200, blank=True)

    
class PoBoxAddress(GeographicAddress):
    box_number = models.CharField(max_length=200, blank=True)
    locality = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return "PO Box {}, {}".format(self.box_number, self.locality)

    
class LocalAddress(Place):
    geographic_address_content_type = models.ForeignKey(ContentType, related_name="%(app_label)s_%(class)s_ownership", blank=True, null=True) 
    geographic_address_object_id = models.PositiveIntegerField(blank=True, null=True)
    geographic_address = GenericForeignKey('geographic_address_content_type', 'geographic_address_object_id')

    full_address = models.CharField(max_length=250, blank=True)
    position_number = models.CharField(max_length=50, blank=True)
    type = models.CharField(max_length=150, blank=True)

    class Meta:
        abstract = True
        
        
class AbsoluteLocalLocation(LocalAddress):
    x = models.CharField(max_length=30)
    y = models.CharField(max_length=30)
    z = models.CharField(max_length=30)


country_codes = """ABW|Aruba^AFG|Afghanistan^AGO|Angola^AIA|Anguilla^ALA|Åland Islands^ALB|Albania^AND|Andorra^ARE|United Arab Emirates^ARG|Argentina^ARM|Armenia^ASM|American Samoa^ATA|Antarctica^ATF|French Southern Territories^ATG|Antigua and Barbuda^AUS|Australia^AUT|Austria^AZE|Azerbaijan^BDI|Burundi^BEL|Belgium^BEN|Benin^BES|Bonaire, Sint Eustatius and Saba^BFA|Burkina Faso^BGD|Bangladesh^BGR|Bulgaria^BHR|Bahrain^BHS|Bahamas^BIH|Bosnia and Herzegovina^BLM|Saint Barthélemy^BLR|Belarus^BLZ|Belize^BMU|Bermuda^BOL|Bolivia, Plurinational State of^BRA|Brazil^BRB|Barbados^BRN|Brunei Darussalam^BTN|Bhutan^BVT|Bouvet Island^BWA|Botswana^CAF|Central African Republic^CAN|Canada^CCK|Cocos (Keeling) Islands^CHE|Switzerland^CHL|Chile^CHN|China^CIV|Côte d'Ivoire^CMR|Cameroon^COD|Congo, the Democratic Republic of the^COG|Congo^COK|Cook Islands^COL|Colombia^COM|Comoros^CPV|Cabo Verde^CRI|Costa Rica^CUB|Cuba^CUW|Curaçao^CXR|Christmas Island^CYM|Cayman Islands^CYP|Cyprus^CZE|Czech Republic^DEU|Germany^DJI|Djibouti^DMA|Dominica^DNK|Denmark^DOM|Dominican Republic^DZA|Algeria^ECU|Ecuador^EGY|Egypt^ERI|Eritrea^ESH|Western Sahara^ESP|Spain^EST|Estonia^ETH|Ethiopia^FIN|Finland^FJI|Fiji^FLK|Falkland Islands (Malvinas)^FRA|France^FRO|Faroe Islands^FSM|Micronesia, Federated States of^GAB|Gabon^GBR|United Kingdom^GEO|Georgia^GGY|Guernsey^GHA|Ghana^GIB|Gibraltar^GIN|Guinea^GLP|Guadeloupe^GMB|Gambia^GNB|Guinea-Bissau^GNQ|Equatorial Guinea^GRC|Greece^GRD|Grenada^GRL|Greenland^GTM|Guatemala^GUF|French Guiana^GUM|Guam^GUY|Guyana^HKG|Hong Kong^HMD|Heard Island and McDonald Islands^HND|Honduras^HRV|Croatia^HTI|Haiti^HUN|Hungary^IDN|Indonesia^IMN|Isle of Man^IND|India^IOT|British Indian Ocean Territory^IRL|Ireland^IRN|Iran, Islamic Republic of^IRQ|Iraq^ISL|Iceland^ISR|Israel^ITA|Italy^JAM|Jamaica^JEY|Jersey^JOR|Jordan^JPN|Japan^KAZ|Kazakhstan^KEN|Kenya^KGZ|Kyrgyzstan^KHM|Cambodia^KIR|Kiribati^KNA|Saint Kitts and Nevis^KOR|Korea, Republic of^KWT|Kuwait^LAO|Lao People's Democratic Republic^LBN|Lebanon^LBR|Liberia^LBY|Libya^LCA|Saint Lucia^LIE|Liechtenstein^LKA|Sri Lanka^LSO|Lesotho^LTU|Lithuania^LUX|Luxembourg^LVA|Latvia^MAC|Macao^MAF|Saint Martin (French part)^MAR|Morocco^MCO|Monaco^MDA|Moldova, Republic of^MDG|Madagascar^MDV|Maldives^MEX|Mexico^MHL|Marshall Islands^MKD|Macedonia, the former Yugoslav Republic of^MLI|Mali^MLT|Malta^MMR|Myanmar^MNE|Montenegro^MNG|Mongolia^MNP|Northern Mariana Islands^MOZ|Mozambique^MRT|Mauritania^MSR|Montserrat^MTQ|Martinique^MUS|Mauritius^MWI|Malawi^MYS|Malaysia^MYT|Mayotte^NAM|Namibia^NCL|New Caledonia^NER|Niger^NFK|Norfolk Island^NGA|Nigeria^NIC|Nicaragua^NIU|Niue^NLD|Netherlands^NOR|Norway^NPL|Nepal^NRU|Nauru^NZL|New Zealand^OMN|Oman^PAK|Pakistan^PAN|Panama^PCN|Pitcairn^PER|Peru^PHL|Philippines^PLW|Palau^PNG|Papua New Guinea^POL|Poland^PRI|Puerto Rico^PRK|Korea, Democratic People's Republic of^PRT|Portugal^PRY|Paraguay^PSE|Palestine, State of^PYF|French Polynesia^QAT|Qatar^REU|Réunion^ROU|Romania^RUS|Russian Federation^RWA|Rwanda^SAU|Saudi Arabia^SDN|Sudan^SEN|Senegal^SGP|Singapore^SGS|South Georgia and the South Sandwich Islands^SHN|Saint Helena, Ascension and Tristan da Cunha^SJM|Svalbard and Jan Mayen^SLB|Solomon Islands^SLE|Sierra Leone^SLV|El Salvador^SMR|San Marino^SOM|Somalia^SPM|Saint Pierre and Miquelon^SRB|Serbia^SSD|South Sudan^STP|Sao Tome and Principe^SUR|Suriname^SVK|Slovakia^SVN|Slovenia^SWE|Sweden^SWZ|Swaziland^SXM|Sint Maarten (Dutch part)^SYC|Seychelles^SYR|Syrian Arab Republic^TCA|Turks and Caicos Islands^TCD|Chad^TGO|Togo^THA|Thailand^TJK|Tajikistan^TKL|Tokelau^TKM|Turkmenistan^TLS|Timor-Leste^TON|Tonga^TTO|Trinidad and Tobago^TUN|Tunisia^TUR|Turkey^TUV|Tuvalu^TWN|Taiwan, Province of China^TZA|Tanzania, United Republic of^UGA|Uganda^UKR|Ukraine^UMI|United States Minor Outlying Islands^URY|Uruguay^USA|United States of America^UZB|Uzbekistan^VAT|Holy See (Vatican City State)^VCT|Saint Vincent and the Grenadines^VEN|Venezuela, Bolivarian Republic of^VGB|Virgin Islands, British^VIR|Virgin Islands, U.S.^VNM|Viet Nam^VUT|Vanuatu^WLF|Wallis and Futuna^WSM|Samoa^YEM|Yemen^ZAF|South Africa^ZMB|Zambia^ZWE|Zimbabwe"""
def import_countries(codes):
    for country in codes.split('^'):
        code, name = country.split('|')
        Country.objects.get_or_create( code=code, name=name )