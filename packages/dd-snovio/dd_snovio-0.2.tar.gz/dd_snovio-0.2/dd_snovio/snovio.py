"""Handles the snovio.io API"""

from typing import Optional, List, Dict
import asyncio
import requests
import aiohttp


class Snovio:
    """
    A Python library designed to handle snovioAPI requests
    using normal and async requests.
    To use async requests user should firstly
    create an instance of the async loop using:
    loop = asyncio.get_event_loop().
    Afterwards user can use the async_requests
    function to handle multiple requests:
    responses = loop.run_until_complete(snovioapi_class_instance.async_requests(
             snovioapi_class_instance.async_function, loop, data))

    async_function - asynchronous function to perform
    loop - asyncio.get_event_loop()
    data - data to send, should be a list or list of dicts,
            it depends on the type of async function.

    Note, the API rate is limited to 60 requests per minute.
    """

    SNOVIOAPI_ADD_URL_FOR_SEARCH = 'https://api.snov.io/v1/add-url-for-search'
    SNOVIOAPI_GET_EMAILS_FROM_URL = 'https://api.snov.io/v1/get-emails-from-url'
    SNOVIOAPI_GET_ACCESS_TOKEN = 'https://api.snov.io/v1/oauth/access_token'
    SNOVIOAPI_GET_DOMAIN_SEARCH = 'https://api.snov.io/v2/domain-emails-with-info'
    SNOVIOAPI_EMAIL_COUNT = 'https://api.snov.io/v1/get-domain-emails-count'
    SNOVIOAPI_GET_EMAIL_FINDER = 'https://api.snov.io/v1/get-emails-from-names'
    SNOVIOAPI_ADD_NAMES_TO_FIND_EMAILS = 'https://api.snov.io/v1/add-names-to-find-emails'
    SNOVIOAPI_GET_PROFILE_BY_EMAIL = 'https://api.snov.io/v1/get-profile-by-email'
    SNOVIOAPI_GET_EMAIL_VERIFIER = 'https://api.snov.io/v1/get-emails-verification-status'
    SNOVIOAPI_ADD_EMAILS_FOR_VERIFICATION = 'https://api.snov.io/v1/add-emails-to-verification'
    SNOVIOAPI_GET_BALANCE = 'https://api.snov.io/v1/get-balance'
    SNOVIOAPI_ADD_PROSPECT_TO_LIST = 'https://api.snov.io/v1/add-prospect-to-list'
    SNOVIO_GET_PROSPECT_BY_ID = 'https://api.snov.io/v1/get-prospect-by-id'
    SNOVIO_GET_PROSPECT_BY_EMAIL = 'https://api.snov.io/v1/get-prospects-by-email'
    SNOVIOAPI_FIND_PROSPECTS_CUSTOM_FIELD = 'https://api.snov.io/v1/prospect-custom-fields'
    SNOVIOAPI_SEE_USER_LISTS = 'https://api.snov.io/v1/get-user-lists'
    SNOVIOAPI_VIEW_PROSPECTS_IN_LIST = 'https://api.snov.io/v1/prospect-list'
    SNOVIOAPI_CREATE_NEW_PROSPECT_LIST = 'https://api.snov.io/v1/lists'

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = self.get_access_token()
        self.delay = 0.1
        self.next_delay = 0

    def set_request_delay(self, requests_delay):
        """ Enables user to set request delay time
            :param requests_delay: delay time between requests
        """
        self.delay = requests_delay

    async def async_requests(self, function, async_loop, data) -> Optional[List[Dict]]:
        """Function responsible for handling async requests.

            :param function: asynchronous function to perform
            :param async_loop: loop instance of the async requests
            :param data: data to send
        """

        output = await asyncio.gather(
            *[function(async_loop, element) for element in data], return_exceptions=True)
        self.next_delay = 0
        return output

    def get_access_token(self) -> Optional[str]:
        """Returns an access token to snovio API
            Price: Free
            Limits: No
            :return snovio response with access token
        """

        body = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }

        response = requests.post(self.SNOVIOAPI_GET_ACCESS_TOKEN,
                                 data=body)

        access_token = response.json()['access_token']
        return access_token if response.status_code != 204 else None

    def get_domain_search(self, domain_name, last_id) -> Optional[List[Dict]]:
        """ Enter a domain name and Snov.io will return all the email addresses on the domain.
            If there is any additional information about the email owner available in the database,
            we will add it as well. Each response returns up to 100 emails. If it does not return
            at least one email, you will not be charged for the request.
            Price: 1 credit per 10 emails/prospects
            Limits: No
            :param domain_name: name of domain to get prospect from
            :param last_id: id of the last prospect in previous request
            :return snovio response with prospect
        """
        body = {
            'access_token': self.access_token,
            'domain': domain_name,
            'type': 'all',
            'limit': 100,
            'lastId': last_id,
            'positions[]': ['Software Developer', 'QA']
        }

        response = requests.get(self.SNOVIOAPI_GET_DOMAIN_SEARCH, json=body)
        return response.json() if response.status_code != 204 else None

    def get_email_count(self, domain_name) -> Optional[dict]:
        """ With this API method, you can find out the number of email addresses
            from a certain domain in our database.
            Price: Free
            Limits: No
            :param domain_name: name of domain to get prospect from
            :return snovio response with dictionary containing the result
        """
        body = {'access_token': self.access_token,
                'domain': domain_name
                }

        response = requests.post(self.SNOVIOAPI_EMAIL_COUNT, data=body)

        return response.json() if response.status_code != 204 else None

    async def async_get_email_finder(self, loop, person) -> Optional[Dict]:
        """Sends async request to get prospect from snovio API.
            This API method finds email addresses using the person`s
            first and last name, and a domain name. If we don`t have
            this email address in our database, we won`t be able to
            provide the results to you right away. To speed up the
            process, you can use the Add Names To Find Emails method
            to push this email address for search. After that, try the
            Email Finder method again.
            Price: Free
            Limits: Yes
            :param loop: loop instance of the async requests
            :param person: dictionary containing information about the person:
                            "domain_name", "first_name", "second_name"
            :return snovio response with the prospect
        """

        body = {'access_token': self.access_token,
                'domain': person["domain_name"],
                'firstName': person["first_name"],
                'lastName': person["second_name"]
                }

        self.next_delay += self.delay
        await asyncio.sleep(self.next_delay)

        async with aiohttp.ClientSession(loop=loop) as session, \
                session.post(self.SNOVIOAPI_GET_EMAIL_FINDER,
                             data=body, ssl=False) as resp:
            response = await resp.json()
        return response if resp.status != 204 else None

    async def async_add_names_to_find_emails(self, loop, person) -> Optional[Dict]:
        """Sends async request to check if person is in snovio database.
            If Snov.io does not have the emails you are looking for in its
            database and can't provide these email addresses via the Email finder,
            you can try to push the request for email search using this method.
            If an email is found, you can collect it by using the free Email finder
            request again.
            Price: 1 credit per request
            Limits: No
            :param loop: loop instance of async requests
            :param person: dictionary containing information about the person:
                            "domain_name", "first_name", "second_name"
            :return snovio response with information about prospect availability
        """

        body = {'access_token': self.access_token,
                'domain': person["domain_name"],
                'firstName': person["first_name"],
                'lastName': person["second_name"]
                }

        self.next_delay += self.delay
        await asyncio.sleep(self.next_delay)

        async with aiohttp.ClientSession(loop=loop) as session, \
                session.post(self.SNOVIOAPI_GET_EMAIL_FINDER,
                             data=body, ssl=False) as resp:
            response = await resp.json()
        return response if resp.status != 204 else None

    async def async_add_url_for_search(self, loop, profile_url) -> Optional[Dict]:
        """Prepares an url to be used in the snovio search engine.
            Find prospects by social URL. To receive the results, use
            the Get prospect with URL method.
            Price: 1 credit per request
            Limits: No
            :param loop: loop instance of async requests
            :param profile_url: url to social profile
            :return snovio response with information about the prospect
        """

        body = {'access_token': self.access_token,
                'url': profile_url
                }

        self.next_delay += self.delay
        await asyncio.sleep(self.next_delay)

        async with aiohttp.ClientSession(loop=loop) as session, \
                session.post(self.SNOVIOAPI_ADD_URL_FOR_SEARCH,
                             data=body, ssl=False) as resp:
            response = await resp.json()
        return response if resp.status != 204 else None

    async def async_get_prospect_from_url(self, loop, profile_url) -> Optional[Dict]:
        """Sends async request to get prospect from snovio API using social URL
            Price: Free
            Limits: No
            :param loop: loop instance of async requests
            :param profile_url: url to social profile
            :return snovio response with the prospect
        """

        body = {'access_token': self.access_token,
                'url': profile_url
                }

        self.next_delay += self.delay
        await asyncio.sleep(self.next_delay)

        async with aiohttp.ClientSession(loop=loop) as session, \
                session.post(self.SNOVIOAPI_GET_EMAILS_FROM_URL,
                             data=body, ssl=False) as resp:
            response = await resp.json()
        return response if resp.status != 204 else None

    async def async_get_profile_by_email(self, loop, email_address) -> Optional[Dict]:
        """Sends async request to get prospect from snovio API using email.
            Provide an email address and Snov.io will return all the profile
            information connected to the provided email address owner from
            the database. If we find no information about the email owner in
            our database, you will not be charged for the request.
            Price: 1 credit per request
            Limits: No
            :param loop: loop instance of async requests
            :param email_address: an email of the selected person
            :return snovio response with the prospect
        """

        body = {'access_token': self.access_token,
                'email': email_address
                }

        self.next_delay += self.delay
        await asyncio.sleep(self.next_delay)

        async with aiohttp.ClientSession(loop=loop) as session, \
                session.post(self.SNOVIOAPI_GET_EMAILS_FROM_URL,
                             data=body, ssl=False) as resp:
            response = await resp.json()
        return response if resp.status != 204 else None

    def get_email_verifier(self, emails) -> Optional[Dict]:
        """ Check if the provided email addresses are valid and deliverable.
            API endpoint will return the email verification results. If we
            haven’t verified a certain email address before, the results
            will not be returned to you. In this case, the API will return
            a “not_verified” identifier and you will not be charged credits
            for this email. You should use the Add emails for verification
            method to push this email address for verification, after which
            you will be able to get the email verification results using this
            endpoint.
            Price: Free
            Limits: No
            :param emails: emails to verify
            :return snovio response with dictionary containing the results
        """
        body = {'access_token': self.access_token}

        url_request = self.SNOVIOAPI_GET_EMAIL_VERIFIER + '?'
        for email in emails:
            url_request = url_request + "emails[]=" + email + '&'
        url_request = url_request[:-1]

        response = requests.post(url_request, data=body)

        return response.json() if response.status_code != 204 else None

    def add_emails_for_verification(self, emails) -> Optional[Dict]:
        """ If you've never verified a certain email address before,
            you should push it for verification using this API method.
            After performing this action, you can receive the verification
            results using the Email verifier.
            Price: 0.5 credit per email address
            Limits: No
            :param emails: emails to verify
            :return snovio response with dictionary containing the results
        """
        body = {'access_token': self.access_token}

        url_request = self.SNOVIOAPI_GET_EMAIL_VERIFIER + '?'
        for email in emails:
            url_request = url_request + "emails[]=" + email + '&'
        url_request = url_request[:-1]

        response = requests.post(url_request, data=body)

        return response.json() if response.status_code != 204 else None

    def get_balance(self) -> Optional[Dict]:
        """ Use this method to check your credit balance.
            Price: Free
            Limits: No
            :return snovio response with dictionary containing the results
        """

        body = {'access_token': self.access_token}

        response = requests.get(self.SNOVIOAPI_GET_BALANCE, data=body)

        return response.json() if response.status_code != 204 else None

    async def async_add_prospect_to_list(self, loop, prospect) -> Optional[Dict]:
        """Sends async request to add prospect to list.
            Add prospect to a specific list. This method will
            be useful for those who want to automate adding
            prospects to lists with active email drip campaigns.
            This way after a prospect is automatically added to
            a chosen list, an email drip campaign will be started
            for them automatically.
            person = {'email':'john.doe@example.com',
              'fullName': 'John Doe',
              'firstName':'John',
              'lastName':'Doe',
              'country':'United States',
              'locality':'Woodbridge, New Jersey',
              'socialLinks[linkedIn]':'https://www.linkedin.com/in/johndoe/&social',
              'social[twiiter]':'https://twitter.com/johndoe&social',
              'position':'Vice President of Sales',
              'companyName':'GoldenRule',
              'companySite':'https://goldenrule.com',
              'updateContact':1
              'listId': 323231
            }
            Price: Free
            Limits: No
            :param loop: loop instance of the async requests
            :param prospect: information about the person
            :return snovio response with information about the result
        """

        body = {'access_token': self.access_token,
                'email': prospect['email'],
                'fullName': prospect['fullName'],
                'firstName': prospect['firstName'],
                'lastName': prospect['lastName'],
                'country': prospect['country'],
                'locality': prospect['locality'],
                'socialLinks[linkedIn]': prospect['linkedIn'],
                'social[twiiter]': prospect['twitter'],
                'position': prospect['position'],
                'companyName': prospect['companyName'],
                'companySite': prospect['companySite'],
                'updateContact': prospect['updateContact'],
                'listId': prospect['list_id']
                }

        self.next_delay += self.delay
        await asyncio.sleep(self.next_delay)

        async with aiohttp.ClientSession(loop=loop) as session, \
                session.post(self.SNOVIOAPI_ADD_PROSPECT_TO_LIST,
                             data=body, ssl=False) as resp:
            response = await resp.json()
        return response if resp.status != 204 else None

    async def async_get_prospect_by_id(self, loop, prospect_id) -> Optional[Dict]:
        """Sends async request to get prospect from snovio.
            Find prospects from your lists by id. Knowing
            the id of a specific prospect you can get full
            information on the prospect, including the lists
            and campaigns they’ve been added to.
            Price: Free
            Limits: No
            :param loop: loop instance of async requests
            :param prospect_id: id of the prospect in snovio
            :return snovio response with the prospect
        """

        body = {'access_token': self.access_token,
                'id': prospect_id
                }

        self.next_delay += self.delay
        await asyncio.sleep(self.next_delay)

        async with aiohttp.ClientSession(loop=loop) as session, \
                session.post(self.SNOVIO_GET_PROSPECT_BY_ID,
                             data=body, ssl=False) as resp:
            response = await resp.json()
        return response if resp.status != 204 else None

    async def async_get_prospect_by_email(self, loop, email) -> Optional[Dict]:
        """Sends async request to get prospect from snovio.
            Find prospect from your lists by email address.
            When you search by email, you receive a list of
            all prospects tied to this email address. Every
            element of the list contains full information on
            the prospect, including the lists and campaigns
            they’ve been added to.
            Price: Free
            Limits: No
            :param loop: loop instance of the async requests
            :param email: email of the prospect in snovio
            :return snovio response with the prospect
        """

        body = {'access_token': self.access_token,
                'email': email
                }

        self.next_delay += self.delay
        await asyncio.sleep(self.next_delay)

        async with aiohttp.ClientSession(loop=loop) as session, \
                session.post(self.SNOVIO_GET_PROSPECT_BY_EMAIL,
                             data=body, ssl=False) as resp:
            response = await resp.json()
        return response if resp.status != 204 else None

    def custom_fields(self) -> Optional[Dict]:
        """ This method returns a list of all custom fields created by the
            user, including the fields’ name, whether the field is optional
            or required, and the field’s data type.
            Price: Free
            Limits: No
            :return snovio response with information about custom fields
        """
        body = {'access_token': self.access_token}

        response = requests.get(self.SNOVIOAPI_FIND_PROSPECTS_CUSTOM_FIELD, data=body)

        return response.json() if response.status_code != 204 else None

    def user_lists(self) -> Optional[Dict]:
        """ This method returns all lists created by the user. You can
            use this method to review lists that can be used for an email
            drip campaign.
            Price: Free
            Limits: No
            :return snovio response with information about lists
        """
        body = {'access_token': self.access_token}

        response = requests.get(self.SNOVIOAPI_SEE_USER_LISTS, data=body)

        return response.json() if response.status_code != 204 else None

    def prospect_in_list(self, list_id, start_page, stop_page) -> Optional[Dict]:
        """ This method returns all the data on prospects in a specific
            list, including prospect’s data like email addresses and their
            status.
            Price: Free
            Limits: No
            :param stop_page: page of list to start downloading prospects
            :param start_page: page of list to stop downloading prospects
            :param list_id: id of the list to get prospects from
            :return snovio response with prospects in list
        """
        body = {'access_token': self.access_token,
                'listID': list_id,
                'page': start_page,
                'perPage': stop_page
                }

        response = requests.post(self.SNOVIOAPI_VIEW_PROSPECTS_IN_LIST, data=body)

        return response.json() if response.status_code != 204 else None

    def add_prospect_list(self, list_name) -> Optional[Dict]:
        """ Use this method to create new prospect lists in your account.
            Price: Free
            Limits: No
            :param list_name: name of the list to create
            :return snovio response with prospects in list
        """
        body = {'access_token': self.access_token,
                'name': list_name
                }

        response = requests.post(self.SNOVIOAPI_CREATE_NEW_PROSPECT_LIST, data=body)

        return response.json() if response.status_code != 204 else None
