login_example site

This example website demonstrates how to create a web application 
with password protected content.
	
This example will use a MySQL or MariaDB database to store users, 
groups, and roles.  Included with this example is a SQL file 
containing the basic table structure for this application.

The example also includes a database configuration file in:
conf/settings/db.cfg

This file is configured to connect to a database named webyaml 
with the database user webyaml and the password webyaml.  This is 
only and example and It is reccomended to use different credentials
in a production enviornment.

After setting up your database, you will still need to add a group,
role and user before you can login.  The easiest way to do this is
to temporarily disable the bouncer in the the file:
conf/template_private.cfg

The bouncer is a preprocessor that checks for logged in users.  If a
logged in user is not found then the bouncer redirects the visitor
to the login page.

To disable the bouncer change this:
	# Comment out the bouncer to add your first user
	-
		**bouncer

to this:

	# Comment out the bouncer to add your first user
	#-
	#	**bouncer
	
After making this change you can reach the private area without a
username and password.  Start by accessing the dashboard at a url
like this one: http://<domain or ip address>:<port>/admin/dashboard

Look for the Managment menu in the header and create a group and role.
After creating at least one group and one role you can create a user.

Notes:

Don't forget to uncomment out the lines above to reenable the bouncer.

If you would like to have a public and a private area for your 
website you can make a new template based on template_login.cfg.  This 
template does not use the bouncer.  Pages built with this template will 
not require a logged in user.

In the file conf/urls.cfg there is an alias url of "/" for the login 
page.  If you want the root page of your application to be something
other than the login page, comment out this alias and define a new page
to serve as "/".
