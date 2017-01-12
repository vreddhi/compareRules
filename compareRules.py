'''
This is authored by Vreddhi Bhat. You can reach out to
vbhat@akamai.com in case of any assistance regarding this code.
'''

import requests, logging, json, sys
from akamai.edgegrid import EdgeGridAuth
import urllib
import json
import configparser
import os
import generateHtml



config = configparser.ConfigParser()
config.read('config.txt')
client_token = config['CREDENTIALS']['client_token']
client_secret = config['CREDENTIALS']['client_secret']
access_token = config['CREDENTIALS']['access_token']
access_url = config['CREDENTIALS']['access_url']

prodDigitalProperty = config['PROD_PROPERTY']['configuration_name']
qaDigitalProperty = config['QA_PROPERTY']['configuration_name']
devDigitalProperty = config['DEV_PROPERTY']['configuration_name']

prodVersion = config['PROD_PROPERTY']['version']
qaVersion = config['QA_PROPERTY']['version']
devVersion = config['DEV_PROPERTY']['version']

output_file_name = config['OTHERS']['filename']


class PapiObjects(object):
    session = requests.Session()
    baseUrl = access_url+'/papi/v0'
    propertyFound = "NOT_FOUND"
    propertyDetails = {}

    print("\nEstablishing connection and authenticating the user\n")
    session.auth = EdgeGridAuth(
				client_token = client_token,
				client_secret = client_secret,
				access_token = access_token
                )
    print("Connection Established.\n")


    def getContracts(self):
        contractUrl = self.baseUrl + '/contracts'
        contractResponse = self.session.get(contractUrl)

    def getGroup(self):
        groupUrl = self.baseUrl + '/groups/'
        groupResponse = self.session.get(groupUrl)
        return groupResponse

    def getRuleNames(self,parentRule,parentruleName,filehandler):
        for eachRule in parentRule:
            ruleName = parentruleName + " --> " + eachRule['name']
            filehandler.writeChildRules(ruleName)
            if len(eachRule['children']) != 0:
                self.getRuleNames(eachRule['children'],ruleName,filehandler)


    def fetchIndividualProperty(self,digitalProperty,ContractId,GroupId,propertyId,version,filehandler):
        print("\nFound "+ digitalProperty + " under contract: "+ContractId[4:]+"")
        print("Please wait while we fetch version: " + version + "'s JSON body\n")
        rulesUrl = self.baseUrl + '/properties/'+propertyId+'/versions/'+ version +'/rules/?contractId='+ContractId+'&groupId='+GroupId
        rulesUrlResponse = self.session.get(rulesUrl)
        rulesUrlJsonResponse = rulesUrlResponse.json()
        try:
            RulesList = rulesUrlJsonResponse['rules']['children']
            ruleNumber = 1
            for eachRule in RulesList:
                filehandler.writeParentRule(str(ruleNumber) + ". " + eachRule['name'])
                ruleNumber += 1
                if len(eachRule['children']) != 0:
                    ruleName = eachRule['name']
                    self.getRuleNames(eachRule['children'],ruleName,filehandler)
        except KeyError:
            print("Looks like there are no rules other than default rule")

    def getProperties(self,contractId,groupId):
        #contractId and groupId are list item here
        propertiesList = []
        url = self.baseUrl + '/properties/' + '?contractId=' + contractId[0]+'&groupId=' + groupId[0]
        propertiesResponse = self.session.get(url)
        if propertiesResponse.status_code == 200:
            propertiesResponseJson = propertiesResponse.json()
            propertiesList = propertiesResponseJson['properties']['items']
        return propertiesList


################################################
#####  Program Execution starts here  ##########
################################################

filehandler = generateHtml.htmlWriter(output_file_name)
filehandler.writeData(filehandler.start_data)
papiObj = PapiObjects()
papiObj.getContracts()
print("Fetching all the contracts and groups\n")
groupsInfo = papiObj.getGroup()
groupsInfoJson = groupsInfo.json()
groupItems = groupsInfoJson['groups']['items']
print("Please hold on while we fetch the properties/Configurations..... This will take time..\n")
for item in groupItems:
    if not 'prodConfigFound' 'qaConfigFound' 'devConfigFound' in locals():
        try:
            contractId = [item['contractIds'][0]]
            groupId = [item['groupId']]
            propertiesList = papiObj.getProperties(contractId,groupId)
            if len(propertiesList):
                for propertyInfo in propertiesList:
                    propertyName = propertyInfo['propertyName']
                    propertyId = propertyInfo['propertyId']
                    propertyContractId = propertyInfo['contractId']
                    propertyGroupId = propertyInfo['groupId']
                    papiObj.propertyDetails[propertyName] = propertyName #This is used to populate all property names
                    if propertyName == prodDigitalProperty or propertyName == prodDigitalProperty+".xml":
                        prodConfigFound = 1
                        filehandler.writeData(filehandler.div_start_data)
                        filehandler.writeTableHeader(prodDigitalProperty)
                        papiObj.fetchIndividualProperty(prodDigitalProperty,propertyContractId,propertyGroupId,propertyId,prodVersion,filehandler)
                        filehandler.writeData(filehandler.div_end_data)
                        print("Looking for a configuration now... Hold on...\n")
                    elif propertyName == qaDigitalProperty or propertyName == qaDigitalProperty+".xml":
                        qaConfigFound = 1
                        filehandler.writeData(filehandler.div_start_data)
                        filehandler.writeTableHeader(qaDigitalProperty)
                        papiObj.fetchIndividualProperty(qaDigitalProperty,propertyContractId,propertyGroupId,propertyId,qaVersion,filehandler)
                        filehandler.writeData(filehandler.div_end_data)
                        print("Looking for a configuration now... Hold on...\n")
                    elif propertyName == devDigitalProperty or propertyName == devDigitalProperty+".xml":
                        devConfigFound = 1
                        filehandler.writeData(filehandler.div_start_data)
                        filehandler.writeTableHeader(devDigitalProperty)
                        papiObj.fetchIndividualProperty(devDigitalProperty,propertyContractId,propertyGroupId,propertyId,devVersion,filehandler)
                        filehandler.writeData(filehandler.div_end_data)
                        print("Looking for a configuration now... Hold on...\n")
        except KeyError:
            continue

if not 'prodConfigFound' in locals():
    print("\n" + prodDigitalProperty + " is not Found under any contract and group" + "\n")
elif not 'qaConfigFound' in locals():
    print("\n" + qaDigitalProperty + " is not Found under any contract and group" + "\n")
elif not 'devConfigFound' in locals():
    print("\n" + devDigitalProperty + " is not Found under any contract and group" + "\n")

print("\nA comparison document is saved as comparedData.html, if configurations were valid\n")
filehandler.writeData(filehandler.end_data)
