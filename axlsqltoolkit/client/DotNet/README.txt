Copyright  Cisco Systems, Inc.

WSDL-NET README File




This readme file contains information specific to the use of the AXLAPI.wsdl in .NET Environment.
Main.cs requires  AXLAPIService.cs  file to run .

Purpose:

To fix the AXL-SOAP Configurability API’s WSDL and XSD files with the explicit purpose for integration with a .NET client. 



Changes Required:

. Run WSDL.exe

	"wsdl.exe AXLAPI.wsdl axlsoap.xsd" which will result in AXLAPIService.cs.

	Resulting class AXLAPIService in AXLAPIService.cs needs at least three changes:

	a. Create an ICertificatePolicy-derived class which will later be associated with our service. This class is a brute-force approach to policy and certificate management. This is necessary in  AXL due to usage of HTTPS.

	public class BruteForcePolicy : System.Net.ICertificatePolicy
	{
		public bool CheckValidationResult(System.Net.ServicePoint sp, System.Security.Cryptography.X509Certificates.X509Certificate cert,
				System.Net.WebRequest request, int problem)
		{        
		return true;
		}
	}

	b. Modify service constructor to take username/password credentials, CallManager IP as an argument, and associate the BruteForcePolicy class with the static CertificatePolicy manager.

	public AXLAPIService(string ccmIp, string user, string password) 
	{
		System.Net.ServicePointManager.CertificatePolicy = new BruteForcePolicy();

		this.Url = "https://" + ccmIp + ":8443/axl/";
		this.Credentials = new System.Net.NetworkCredential(user, password);
	}

	c. .NET uses the expects header differently (http://issues.apache.org/bugzilla/show_bug.cgi?id=31567). There are some workarounds to this problem as listed below:

		i. Override the GetWebRequest method to use HTTP 1.0 due to error between TOMCAT/AXIS and .NET HTTP 1.1 Web Service request mechanism.  

		protected override System.Net.WebRequest GetWebRequest(Uri uri)
		{
			System.Net.HttpWebRequest request = base.GetWebRequest (uri) as System.Net.HttpWebRequest;
			request.ProtocolVersion = System.Net.HttpVersion.Version10; 

			return request;
		}

		ii. Override the GetWebRequest method to manually embed authentication string.  If you do this, do not use the line
		  this.Credentials = new System.Net.NetworkCredential(user, password); 
		  from the constructor provided in point b of this section.

		protected override System.Net.WebRequest GetWebRequest(Uri uri) 
		{ 
			System.Net.HttpWebRequest request =(System.Net.HttpWebRequest)base.GetWebRequest(uri); 
			if (this.PreAuthenticate) 
			{ 
				System.Net.NetworkCredential nc = this.Credentials.GetCredential(uri,"Basic"); 
				if (nc != null) 
				{ 
					byte[] credBuf = new System.Text.UTF8Encoding().GetBytes(nc.UserName + ":" + nc.Password); 
					request.Headers["Authorization"] = "Basic " + Convert.ToBase64String(credBuf); 
				}
			}
			return request; 
		}

		iii. If using wsdl2wse (WSE library) instead of wsdl.exe, you can not override the HTTP version or supply HTTP headers manually.   If one wants to use WSE, you have to set Keep-Alive header to false for the generated class, or set the user-agent to restricted.  This technique will work in lieu of approach in point i and ii above.

