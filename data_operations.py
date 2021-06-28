
# drop column --> 'Unnamed: 0
    #df_houses.drop('Unnamed: 0', axis=1, inplace=True)

# rename columns:
    '''
    df_houses = df_houses.rename(columns={"Area [m²]" : "area"
      ,"Price [€]" : "price"
      ,"state of the building": "building_state"
      ,"number of facades": "facades"
      ,"number of bedrooms": "bedrooms"
      ,"fully equipped kitchen": "kitchen_equipped"
      ,"open fire": "open_fire"
      ,"locality [zip code]": "locality"
      ,"surface of the land [m²]": "land_surface"
      ,"terrace surface [m²]": "terrace_surface"
      ,"swimming pool": "swimming_pool"
      ,"type of property": "property_type"
      ,"subtype of property": "property_subtype"
      ,"garden surface [m²]": "garden_surface"})
'''
# fix typo:
    #df_houses['property_subtype'] = df_houses['property_subtype'].replace(to_replace='exceptiona', value='exeptional')

