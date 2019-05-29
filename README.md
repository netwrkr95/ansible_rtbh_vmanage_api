## Modifying Cisco vManage with Ansible and REST API's

This is revised code for vManage 18.3.3 REST API's that changed from 17.x, as several requirements changed.  This code targets the use case for operators that target modifying the application-list in a vManage policy to control and/or mitigate the remote trigger blackhole (RTBH) concept.  

### Overview and Use Case

The purpose of the RTBH concept is identifying an application(s) and taking an action for that application across, in this case, the vManage controlled SD-WAN.  For this use case, the operator has the ability to specify the application, from the available applications in the policy, and apply a "scavenger class" or "black hole action" to each of the nodes within the list.  This allows the operator to limit and control specific applications within an enterprise or agency.  If the application is deemed as harmful, the operator can black-hole the traffic based on the policy as an option as well. 

#### vManage Policy Example

Below is a preview the application policy example used:

```
lists
  app-list Suspect_Video_Apps
   app twitter 
   app espn-browsing 
   app espn 
  !
```

Below is a preview of the enforcement action of the application policy "match":

```
  policer DDOS_Scavenger
   burst 1000000
   exceed remark
   rate 500000
  !
```

It should be noted that the operator has the ability, within vManage policy, to modify other key elements that could also be leveraged for this concept, such as VPN's, modification of the site list (for which routers the policy should be enforced on. These are some of the basic examples.


#### Getting Started

This demonstration is leveraging the following versions of code:

```
vManage = version 18.3.3
Ansible = version 2.6.12
```

#### Acknowledgements

I would like to thank Chris Hocker @chrishocker for his large contributions and mentoring for this project.




