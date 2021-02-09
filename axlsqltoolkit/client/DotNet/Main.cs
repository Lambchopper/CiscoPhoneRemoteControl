using System;
using System.Collections.Generic;
using System.Text;
using System.Net;

/*This class has methods which deal with the different simple and
 * complex type elements of 8.0 schema of AXL.
 * 
 * It would give an idea on how the client can set different types like 
 * 
 * -How to set Choice type Ex refer to method callUpdatePhoneToModifyCSS.
 * -How to set XFkType tags  where one can give "value" or "uuid" Ex callUpdatePhoneToModifyCSS
 * -How to set String types :) Ex callExecuteQuery where sql tag is a string type
 * -How to set Members in an ADD api  request  Ex callAddUserGroup
 * -How to set Members in an Update api request , as this tag  comes  as a choice in update api's 
 *  as compared to ADD API    Ex callAddUserGroup
 * -How to use a Get API with returned tags.
 * -How to set a List API with search criteria .
 * -How to use a DoDeviceLogin and DoDeviceReset apis Ex callDoDeviceLogin,callDoDeviceReset methods have  
 *  meta data provided for the User to directly use the methods.
 * 
 * 
 * APIS like ExecuteSQLQuery have been also exposed however processing of the response can be modified accordingly
 * 
 * This class exposes the mostly used APIs 
 */

namespace _8_0
{

    public class Main_8_0
    {
        static void Main(string[] args)
        {
            try
            {  
                string ccmIp = "10.77.31.219";
                string user = "CCMAdministrator";
                string password = "219_axl";

                AXLAPIService axlApiService = new AXLAPIService(ccmIp, user, password);
                axlApiService.ConnectionGroupName = "CUCM:DB ver=8.0";

                callExecuteQuery(axlApiService); 
                callAddPhone(axlApiService);
                callGetPhone(axlApiService);
                callListPhone(axlApiService);
                callDoDeviceLogin(axlApiService);
                callDoDeviceReset(axlApiService);
                callRemovePhone(axlApiService);
                callAddLine(axlApiService);               
                callAddEndUser(axlApiService);              
                callAddDeviceProfile(axlApiService);          
                callAddCallerFilterReq(axlApiService);
                callUpdateCallerFilter(axlApiService);      
                callUpdatePhoneToModifyCSS(axlApiService);
                callAddUserGroup(axlApiService);
               
            }
            catch (NullReferenceException e)
            {
                Console.WriteLine("NullReferenceException");
                Console.WriteLine(e);
            }
            catch (System.Web.Services.Protocols.SoapException e)
            {
                Console.WriteLine(e.Message);                
            }
           
            catch (Exception e)
            {
                Console.WriteLine("Exception");              
                Console.WriteLine(e);
            }
        }



        /*Associating user to a group
         * 
         * ##Values in the method are hardcoded please modify accordingly to make it work###
         */
        private static void callAddUserGroup(AXLAPIService axlApiService)
        {
            AddUserGroupReq request = new AddUserGroupReq();
            request.userGroup = new XUserGroup();
            request.userGroup.name = "NET Group";

            request.userGroup.members = new XUserGroupMembers();
            XUserGroupMember xMember = new XUserGroupMember();
            request.userGroup.members.member = new XUserGroupMember[1];
            xMember.userId = "DotNetuser";

            request.userGroup.members.member.SetValue(xMember, 0);
            StandardResponse response = axlApiService.addUserGroup(request);
            Console.WriteLine("Response  of  callAddUserGroup" + response.@return);

        }


        /*To modify CSS and update line
         * 
         * ##Values in the method are hardcoded please modify accordingly to make it work###
         */
        private static void callUpdatePhoneToModifyCSS(AXLAPIService axlApiService)
        {
            UpdatePhoneReq request = new UpdatePhoneReq();
            request.ItemElementName = ItemChoiceType32.name;
            request.Item = "SEP100000100003";
            XFkType xfkType= new XFkType();
            xfkType.Value = "AXL-CSS0";
            request.callingSearchSpaceName = xfkType;
             request.lines = new UpdatePhoneReqLines();
            request.lines.Items = new XPhoneLine[1];
            XPhoneLine line = new XPhoneLine();
            line.index = "2";
            line.display = "Line32";
            //existing directory number
            line.dirn = new XDirn();
            line.dirn.pattern = "10002";
            xfkType = new XFkType();
            xfkType.Value = "AXL-RP";
            line.dirn.routePartitionName = xfkType;
            request.lines.Items.SetValue(line, 0);
     

            xfkType = new XFkType();
            xfkType.Value = "Standard 7960 SCCP";
            request.phoneTemplateName = xfkType;
            xfkType = new XFkType();
            xfkType.Value = "Cisco 7960 - Standard SCCP Non-Secure Profile";
            request.securityProfileName = xfkType;
            xfkType = new XFkType();
            xfkType.Value = "Default";
            request.devicePoolName = xfkType;
     
            StandardResponse response = axlApiService.updatePhone(request);
            Console.WriteLine("Successfully executed    AXL Update Phone using  UpdatePhoneReq" + response.@return);
        }



        /*
         * 
         * ##Values in the method are hardcoded please modify accordingly to make it work###
         */
        private static void callDoDeviceReset(AXLAPIService axlApiService)
        {
            //metadata  please fill the data
            String strDeviceName = "";        
  
            DoDeviceResetReq request = new DoDeviceResetReq();

            XFkType xfkType = new XFkType();
            xfkType.Value = strDeviceName;
            request.deviceName = xfkType;

            request.ItemElementName = ItemChoiceType34.isHardReset;
            request.Item = "true";
            //If the other choice is required uncomment the lines below
            //And comment out the above lines.
            //request.ItemElementName = ItemChoiceType34.deviceResetType;
            //request.Item ="Reset";
            DoDeviceResetRes response = axlApiService.doDeviceReset(request);
            Console.WriteLine("Successfully executed by   AXL using  DoDeviceReserRequest" + response.@return);
        }


        /*
         * 
         * ##Values in the method are hardcoded please modify accordingly to make it work###
         */
        private static void callDoDeviceLogin(AXLAPIService axlApiService)
        {
            //metadata please fill your data and use it.
            String strDeviceName = "";
            String strLoginDuration = "";
            String strUserId = "";
            String strProfileName = "";


            DoDeviceLoginReq request = new DoDeviceLoginReq();

            XFkType xfkType = new XFkType();
            xfkType.Value = strDeviceName;
            request.deviceName = xfkType;

            request.loginDuration = strLoginDuration;

            xfkType = new XFkType();
            xfkType.Value = strProfileName;
            request.profileName = xfkType;
            request.userId = strUserId;

            DoDeviceLoginRes response = axlApiService.doDeviceLogin(request);
            Console.WriteLine("Successfully executed by   AXL using  DoDeviceLoginRequest" + response.@return);
        }

        /*
         * 
         * ##Values in the method are hardcoded please modify accordingly to make it work###
         */
        private static void callListPhone(AXLAPIService axlApiService)
        {
            ListPhoneReq listPhoneReq = new ListPhoneReq();
            listPhoneReq.searchCriteria = new ListPhoneReqSearchCriteria();
            listPhoneReq.searchCriteria.name = "%";
            listPhoneReq.returnedTags = new LPhone();
            listPhoneReq.returnedTags.name = "";
            listPhoneReq.returnedTags.description = "";
            ListPhoneRes listPhoneRes = axlApiService.listPhone(listPhoneReq);

           int noOfPhonesListed=listPhoneRes.@return.Length;
            Console.WriteLine("number of phones listed  :"+noOfPhonesListed);
            int i = 0;
            while(i<noOfPhonesListed){
                LPhone obj=listPhoneRes.@return[i];
                Console.WriteLine("Phone  ----" + i);
                Console.WriteLine("name " + obj.name);
                Console.WriteLine("description " + obj.description);
              
                i++;
            }
        }


        /* Get Phone API 
         * Gives a hint of using returned tags .
         * 
         * ##Values in the method are hardcoded please modify accordingly to make it work###
         */
        private static void callGetPhone(AXLAPIService axlApiService)
        {
            GetPhoneReq getPhoneReq = new GetPhoneReq();
            getPhoneReq.ItemElementName = ItemChoiceType137.name;
            getPhoneReq.Item = "SEP100000100003";

            getPhoneReq.returnedTags = new RPhone();
            getPhoneReq.returnedTags.name = "";
            getPhoneReq.returnedTags.description = "";
            getPhoneReq.returnedTags.lines = new RPhoneLines();
            getPhoneReq.returnedTags.lines.Items = new RPhoneLine[1];
            RPhoneLine returnedLineTags = new RPhoneLine();
            returnedLineTags.dirn =new RDirn();
            returnedLineTags.dirn.pattern="";
        
            returnedLineTags.dirn.routePartitionName=null;
            returnedLineTags.index = null;
            getPhoneReq.returnedTags.lines.Items.SetValue(returnedLineTags, 0);
            GetPhoneRes getResponse = axlApiService.getPhone(getPhoneReq);


            Console.WriteLine("Successfully retrieving  Phone using  GetPhoneRequest" + getResponse.@return);
            GetPhoneResReturn phoneResReturn = getResponse.@return;
            Console.WriteLine("phone name"+phoneResReturn.phone.name);
            Console.WriteLine("phone description" + phoneResReturn.phone.description);
            int noOfLines=phoneResReturn.phone.lines.Items.Length;
            Console.WriteLine("no of lines associated  " +noOfLines );
            int i=0;
            while (i < noOfLines)
            {
                RPhoneLine xyz = (RPhoneLine)phoneResReturn.phone.lines.Items[i];
                Console.WriteLine("Line ----" + i);
                Console.WriteLine("index of the line " + xyz.index);  
   
                Console.WriteLine("Pattern" + xyz.dirn.pattern);
                Console.WriteLine("RoutePartitionName" + xyz.dirn.routePartitionName);
                i++;
            }
        }


        /* AddDeviceProfile 
         * 
         * A simple AddDevice Profile request with only mandatory tags         * 
         * ##Values in the method are hardcoded please modify accordingly to make it work###
         */
        private static void callAddDeviceProfile(AXLAPIService axlApiService)
        {
            AddDeviceProfileReq addDeviceProfileReq = new AddDeviceProfileReq();
            addDeviceProfileReq.deviceProfile = new XDeviceProfile();

            addDeviceProfileReq.deviceProfile.name = "DeviceNet";
            addDeviceProfileReq.deviceProfile.product="Cisco 7960";
            addDeviceProfileReq.deviceProfile.protocol = "SCCP";
            addDeviceProfileReq.deviceProfile.protocolSide = "User";
            addDeviceProfileReq.deviceProfile.@class = "Device Profile";
            XFkType xfktype = new XFkType();
            xfktype.Value = "SEP555555555555-SCCP-Individual Template";

            addDeviceProfileReq.deviceProfile.phoneTemplateName = xfktype;
            StandardResponse response = axlApiService.addDeviceProfile(addDeviceProfileReq);
            Console.WriteLine("Successfully added DeviceProfile  " + response.@return);

        }


        /*
         * A simple  AddEndUser  request with only mandatory tags
         * ##Values in the method are hardcoded please modify accordingly to make it work##
         */
        private static void callAddEndUser(AXLAPIService axlApiService)
        {
            AddUserReq addUserReq = new AddUserReq();
            addUserReq.user = new XUser();
            addUserReq.user.userid="DotNetuser";
            addUserReq.user.lastName="Visual Studio";
             XFkType xfktype = new XFkType();
            //presenceGroup Name value 
             xfktype.Value = "Standard Presence group";
             //Or the UUID 
             //xfktype.uuid=""
             addUserReq.user.presenceGroupName = xfktype;           
             StandardResponse res2 = axlApiService.addUser(addUserReq);
             Console.WriteLine("Successfully added an User using  AddEndUserRequest" + res2.@return);
            
        }
        /* AddLine API
         *  Simple Adding of  a line with mandatory tags         * 
         * ##Values in the method are hardcoded please modify accordingly to make it work###
         */
        private static void callAddLine(AXLAPIService axlApiService)
        {
            AddLineReq addLineReq = new AddLineReq();
            addLineReq.line = new XLine();
            addLineReq.line.pattern = "9999";
            addLineReq.line.description = "Adding a line from .NetClient";
            addLineReq.line.usage = "Device";          
            XFkType xfktype = new XFkType();
            //routepartion value 
             xfktype.Value = "";
             addLineReq.line.routePartitionName = xfktype;
            StandardResponse res2 = axlApiService.addLine(addLineReq);
            Console.WriteLine("Successfully added an Line using  of AddLineRequest" + res2.@return); 
        }

        /*
         * Remove API with name mentioned
         * 
         *  Simple callRemovePhone request  with mandatory tags 
         * ##Values in the method are hardcoded please modify accordingly to make it work###
         */
        private static void callRemovePhone(AXLAPIService axlApiService)
        {
            NameAndGUIDRequest removePhoneReq = new NameAndGUIDRequest();
            removePhoneReq.ItemElementName = ItemChoiceType32.name;
            removePhoneReq.Item = "SEP170000100002";
            axlApiService.removePhone(removePhoneReq);

        }



        /* To invoke thin axl from .Net client
         * ExecuteSQLQuery
         * Simple RemovePhone request  with mandatory tags 
         * ##Values in the method are hardcoded please modify accordingly to make it work###
         */
        private static void callExecuteQuery(AXLAPIService axlApiService)
        {
            ExecuteSQLQueryReq exec = new ExecuteSQLQueryReq();
            exec.sql = "select * from typestatus";
            ExecuteSQLQueryRes  resp=axlApiService.executeSQLQuery(exec);
            Console.WriteLine("end of the callExecuteQuery" + resp.@return);
            int i=0;
            Console.WriteLine("Number Of Rows Of Data retrived"+resp.@return.Length);           
            while (i < resp.@return.Length)
            {
             System.Xml.XmlNode []xmlNode = (System.Xml.XmlNode[])resp.@return[i];
             int noChildNodes = xmlNode.Length;
                int j = 0;
                Console.WriteLine("<row>");  
                while (j < noChildNodes)
                {
                    String name=xmlNode[j].Name;
                    String value=xmlNode[j].FirstChild.Value;                   
                    Console.WriteLine("<" + name + ">" + value + "</"+name+">");   
                    j++;
                }
                Console.WriteLine("</row>"); 
                i++;
            }
        }


        /*API to addMembers in add operation
         * 
         * Simple AddCallerFilterReq request  with mandatory tags 
         * ##Values in the method are hardcoded please modify accordingly to make it work###
         */
        private static void callAddCallerFilterReq(AXLAPIService axlApiService)
        {
      
            AddCallerFilterListReq ucflr = new AddCallerFilterListReq();            
            ucflr.callerFilterList = new XCallerFilterList();
            ucflr.callerFilterList.name = "Sriram2";
            ucflr.callerFilterList.description = "testing NET Application1";
            ucflr.callerFilterList.isAllowedType = "true";
            XCallerFilterListMember xmember1 = new XCallerFilterListMember();
            ucflr.callerFilterList.members = new XCallerFilterListMembers();
            ucflr.callerFilterList.members.member = new XCallerFilterListMember[1];       
            xmember1.callerFilterMask = "Directory Number";
            xmember1.DnMask = "663636";
            ucflr.callerFilterList.members.member.SetValue(xmember1, 0);         
            StandardResponse res2 = axlApiService.addCallerFilterList(ucflr);
            Console.WriteLine("end of the callAddCallerFilterReq" + res2.@return);


        }



        /*API to addMembers in update operation
         * 
         * Simple UpdateCallerFilter request  with mandatory tags
         * ###Values in the method are hardcoded please modify accordingly to make it work###
         */
        private static void callUpdateCallerFilter(AXLAPIService axlApiService)
        {   

            UpdateCallerFilterListReq updateObj = new UpdateCallerFilterListReq();  
 
            updateObj.ItemElementName = ItemChoiceType32.name;
            updateObj.Item = "Sriram2";
            
            UpdateCallerFilterListReqAddMembers addMembers = new UpdateCallerFilterListReqAddMembers();
            addMembers.member = new XCallerFilterListMember[1];
            XCallerFilterListMember xmember1 = new XCallerFilterListMember();
            xmember1.callerFilterMask = "Directory Number";
            xmember1.DnMask = "111111";
            addMembers.member.SetValue(xmember1, 0);

            //Create an instance of XCommonMembersExtension
            updateObj.Items =new XCommonMembersExtension[1];
            updateObj.Items.SetValue(addMembers, 0);
       
            StandardResponse res22 = axlApiService.updateCallerFilterList(updateObj);
            Console.WriteLine("end of the callUpdateCallerFilter" + res22.@return);
        }



        /* Add Phone API 
        *  Associating a line with the phone.
        * ( mandatory tags only used to add a phone)
        * ##Values in the method are hardcoded please modify accordingly to make it work###
        */
        private static void callAddPhone(AXLAPIService axlApiService)
        {
            AddPhoneReq addPhoneReq = new AddPhoneReq();
            addPhoneReq.phone = new XPhone();
            addPhoneReq.phone.name = "SEP170000100002";
            addPhoneReq.phone.description = "Adding Phone thru .Net Client";
            addPhoneReq.phone.product = "Cisco 7960";
            addPhoneReq.phone.@class = "Phone";
          
            addPhoneReq.phone.protocol = "SCCP";
            addPhoneReq.phone.protocolSide = "User";

            XFkType xfktype = new XFkType();
            xfktype.Value = "Default";
            addPhoneReq.phone.devicePoolName = xfktype;
            
            xfktype = new XFkType();
            xfktype.Value = "Standard Common Phone Profile";
            addPhoneReq.phone.commonPhoneConfigName = xfktype;
            
            xfktype = new XFkType();
            xfktype.Value = "Hub_None";
            addPhoneReq.phone.locationName = xfktype;
            
            addPhoneReq.phone.useTrustedRelayPoint = "Default";

            addPhoneReq.phone.lines = new XPhoneLines();
            addPhoneReq.phone.lines.Items = new XPhoneLine[1];
            XPhoneLine line = new XPhoneLine();
            line.index = "5";
            line.display = "Line1";
            //existing directory number
            line.dirn = new XDirn();
            line.dirn.pattern = "11233";
            xfktype = new XFkType();
            xfktype.Value = "AXL-RP";
            line.dirn.routePartitionName = xfktype;
            addPhoneReq.phone.lines.Items.SetValue(line, 0);

            StandardResponse res2 = axlApiService.addPhone(addPhoneReq);
            Console.WriteLine("end of the addPhoneReq" + res2.@return);
        }       
    }
}
