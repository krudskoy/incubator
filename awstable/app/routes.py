from flask import render_template, redirect
from app import app
from app.forms import LoginForm
import boto3


aws_access_key_id_var = None
aws_secret_access_key_var = None
aws_region_var = None




@app.route('/', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    global aws_access_key_id_var
    global aws_secret_access_key_var
    global aws_region_var

    if form.validate_on_submit():

        aws_access_key_id_var = form.aws_access_key_id.data
        aws_secret_access_key_var = form.aws_secret_access_key.data
        aws_region_var = form.aws_region.data


        return redirect('/table')


    return render_template('index.html', title='Creds', form=form)

@app.route('/table')
def index():
    client = boto3.client('ec2', region_name = aws_region_var, aws_access_key_id=aws_access_key_id_var,aws_secret_access_key=aws_secret_access_key_var)
    response = client.describe_instances()
    instances = response["Reservations"]

    return render_template('table.html', instances=instances)
