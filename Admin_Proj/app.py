from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify
import ast

app = Flask(__name__)
app.secret_key = 'test123'
app.config['DEBUG'] = True
TEMPLATES_AUTO_RELOAD = True



from tableau_tools.tableau_rest_api import *
from tableau_tools import *
import csv

#version of page that is read only and version that shows command options

username = 'admin'
password = 'admin'
server = 'http://localhost'
site_content_url = 'Default'

server_conn = TableauRestApiConnection28(server, username, password, site_content_url)
server_conn.signin()


#need to add views to delete users from a group, add users to a group, rename a group, duplicate a group, and delete a group

#we can build in logic to add users to check if users are in group already -> jquery grabs existing content from list-group and greys names out if they are there 


@app.route("/", methods=['GET', 'POST'])
def test():
	group_dict = server_conn.convert_xml_list_to_name_id_dict(server_conn.query_groups())
	output_list = []
	for i in group_dict:
	    output = {}
	    output['name'] = i
	    output['luid'] = group_dict[i]
	    user_dict = server_conn.convert_xml_list_to_name_id_dict(server_conn.query_users_in_group(group_dict[i]))
	    member_list = []
	    for elem in user_dict: 
	        member_list.append({'name':elem, 'luid':user_dict[elem]})
	    output['members'] = member_list
	    output_list.append(output)

	return render_template('test.html', output_list=output_list)


@app.route("/delete_group", methods=['POST'])
def delete_group():
	print('lets delete')
	#print(request.form)
	group_id = request.form['luid']
	server_conn.delete_groups([group_id])
	#returning test throws errors...
	return test()

@app.route("/duplicate_group", methods=['POST'])
def duplicate_group():
	group_id = request.form['luid']
	user_id_list = list(server_conn.convert_xml_list_to_name_id_dict(server_conn.query_users_in_group(group_id)).values())
	print('lets duplicate')
	#print(request.form['name'])
	#we wanna get the users for this group
	#user_list = 
	new_name = request.form['name'] + '(1)'
	print (new_name)
	new_luid = server_conn.create_group(new_name)
	server_conn.add_users_to_group(user_id_list, new_luid)
	print(request.form)
	return test()

#havent added error catching like renaming something the same name or too many characters
@app.route("/rename_group", methods=['POST'])
def rename_group():
	group_id = request.form['luid']
	new_name = request.form['new_name']
	print(request.form['new_name'])
	server_conn.update_group(group_id, new_name)
	return test()

@app.route("/add_users", methods=['POST'])
def add_users():
	#print(request.form)
	luid_list = request.form['luid_list']
	group_id = request.form['group_id']
	# print(list(luid_list))
	# print(type(ast.literal_eval(luid_list)))
	luid_list = ast.literal_eval(luid_list)
	# print(group_id)
	server_conn.add_users_to_group(luid_list, group_id)
	return test()


@app.route("/delete_user", methods=['POST'])
def delete_user():
	# print(request.form)
	group_id = request.form['group_luid']
	user_id = request.form['user_luid']
	# print(group_id)
	server_conn.remove_users_from_group(user_id, group_id)
	return redirect(url_for('test'))