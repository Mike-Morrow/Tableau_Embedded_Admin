# Tableau_Embedded_Admin

A single page web application for performing common admin tasks on Tableau Server. Designed for the embedded use case.

The backend uses Flask and leverages Tableau's REST API (via Tableau-Tools) to modify resources on the Tableau Server. The backend is designed to be as minimal as possible, simply passing requests to the Tableau Server and returning JSON objects to the browser that are then parsed into an interactive collapsible list.  

## Motivation:

When embedding Tableau into an existing application, there is a need for the end-users of that application to perform adminstrative tasks (add/remove user, modify groups, etc.) without being aware of or having admin privledges to the Tableau Server (which might btw service various tenants or use cases that the end-user isn't aware of). 




![Alt Text](https://thumbs.gfycat.com/DeadWhirlwindAlaskajingle-size_restricted.gif)
