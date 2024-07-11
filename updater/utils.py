import pandas as pd


def extract_contact_and_account_data(data):

    # required info from cutomerDB
    to_keep = ['plant', 'wanumber', 'businessserviceid',
               'billingmethod', 'dppcentral', 'costcenterkonzernverrechnungskostenstelle', 'summaryreportcontact']

    # for each project extract contact amd account data
    #  contact info and concat to df
    main_contact_channel_df = pd.DataFrame()

    for project in data['data']['getOrganization']['hasProjects']:

        # extract contact data
        project_df = pd.json_normalize(project['hasContactChannels'])
        project_df['project_name'] = project['name']
        project_df['status'] = project['status']
        project_df['hasAccounts'] = len(project['hasAccounts'])

        main_contact_channel_df = pd.concat(
            [main_contact_channel_df, project_df])
        
    # sort contact data, filter relevant accounts
    main_contact_channel_df = main_contact_channel_df.reset_index(drop=True)
    main_contact_channel_df = main_contact_channel_df[main_contact_channel_df.topic == 'BILLING']
    main_contact_channel_df = main_contact_channel_df[main_contact_channel_df.status != 'closed']
    main_contact_channel_df = main_contact_channel_df[main_contact_channel_df.hasAccounts > 0]

    # contact data: extract info from id string
    # split string and drop useless cols
    split_columns = main_contact_channel_df['id'].str.split('#', expand=True)
    main_contact_channel_df.drop(columns=['id', 'topic'], inplace=True)
    split_columns.drop(columns=[0], inplace=True)
    to_rename = {1: "key", 2: "id"}
    split_columns.rename(columns=to_rename, inplace=True)
    split_columns['key'] = split_columns['key'].str.rsplit('_').str[1]

    # join data together. possible because same index
    contacts = main_contact_channel_df.join(split_columns)
    # extarct emails by @ value
    emails = contacts[contacts['value'].str.contains("@")]
    email_lists = emails.groupby('id')['value'].apply(list).reset_index()
    email_lists = pd.merge(email_lists, contacts, on='id').drop(
        columns=['value_y', 'key']).drop_duplicates('id')

    # switch keys to cols
    pivot = contacts.pivot(values='value', columns='key', index='id')
    pivot = pivot[to_keep].reset_index()

    # now check for Nan: return df with bools => False value is Nan
    filter = pivot.groupby('id')[to_keep].apply(
        lambda x: x.notnull().any()).reset_index()

    # merge contact data => add email adresses
    merge_contacts = pd.merge(filter, email_lists, how='left', on='id').rename(
        columns={"value_x": "email_adresses"})

    # add CO email here : if specific value is False => add CO tag. emailadrss comes later in SES lambda
    CO_column = 'billingmethod'
    merge_contacts.loc[merge_contacts[CO_column] == False,
                       'email_adresses'] = merge_contacts['email_adresses'].apply(lambda x: x + ['ClearingOffice'])

    # only retain False values
    merge_contacts['missing_fields'] = merge_contacts.apply(
        lambda x: x.index[x == False].tolist(), axis=1)
    # now drop old cols
    merge_contacts.drop(columns=to_keep+['id'], inplace=True)

    return merge_contacts
