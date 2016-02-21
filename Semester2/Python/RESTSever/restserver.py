from bottle import Bottle,run,request,post,get,delete,put,error
import helper
import json
app = Bottle()
##|----------------------------------------------------------|
##|TO DO:                                                    |
##|      - TESTING ALL THE FUNCTIONS using testrequest.py    |
##|      - To do check helper                                |
##|----------------------------------------------------------|

JBase = helper.JsonBase()
# Method to register a team
@app.post('/robots/<team>')
def register(team):
    try:
        # Try to get the post value
        value = request.forms.get('key',False)
        # If no key posted, send SORRY
        if not value:
            return 'SORRY'
        else:
            # Else try to add the team to the JBase
            ok = JBase.add_team(team,value)
            return 'OK' if ok else 'SORRY'
    except:
        # If anything goes wrong send a SORRY
        return 'SORRY'
# Method to delete a team, the team name and secret key must be specified
@app.delete('/robots/<team>/<secretkey>')
def delete(team,secretkey):
    try:
        # try to delete the team
        ok = JBase.delete_team(team,secretkey)
        # return OK if succes, else return SORRY
        return 'OK' if ok else 'SORRY'
    except:
        # If anything goes wrong send a SORRY
        return 'SORRY'
# A method that returns the map in JSON format
@app.get('/map')
def return_map():
    try:
        return JBase.get_map()
    except:
        return 'SORRY'
# A method that returns the parcels in JSON format
@app.get('/parcels')
def return_parcels():
    try:
        return JBase.get_parcels()
    except:
        return 'SORRY'
# A method for the orders of parcels, only available for secretKey users
@app.put('/parcels/add')
def add_parcels():
    #try:
        secretKey = request.forms.get('secretkey',False)
        if not secretKey:
            return 'SORRY'
        else:
            # Convert to json
            parcels = request.forms.get('newParcels',False)
            print parcels
            if not parcels:
                return 'SORRY'
            else:
                ok = JBase.add_parcels(secretKey,parcels)
                return  'OK' if ok else 'SORRY'
    #except:
        #return 'SORRY'
# A method with which a team can claim a parcel
@app.put('/robots/<team>/claim/<parcel_nb:int>')
def claim_parcel(team,parcel_nb):
    try:
        # Try to get the post value
        value = request.forms.get('key',False)
        # If there is no key specified return SORRY
        if not value:
            return 'SORRY'
        else:
            # Try to claim the parcel given the given key
            ok = JBase.claimmer(parcel_nb,team,value)
        return  'OK' if ok else 'SORRY'
    except:
        return 'SORRY'
# A method with which a team can signal that it has delivered a parcel
@app.put('/robots/<team>/delivered/<parcel-nb:int>')
def deliver_parcel(team):
    try:
        # Try to get the post value
        value = request.forms.get('key',False)
        # If there is no key specified return SORRY
        if not value:
            return 'SORRY'
        else:
            # Try to deliver the parcel
            ok = JBase.deliver(parcel_nb,team,value)
            return  'OK' if ok else 'SORRY'
    except:
        return 'SORRY'
# A method with wich a team can set their current position
@app.put('/positions/<team>/<from_node>/<to_node>')
def set_position(team,from_node,to_node):
    try:
        # Try to get the post value
        value = request.forms.get('key',False)
        # If there is no key specified return SORRY
        if not value:
            return 'SORRY'
        else:
            # Try to update the position
            ok = JBase.update_position(from_node,to_node,team,value)
            return  'OK' if ok else 'SORRY'
    except:
        return 'SORRY'
# A method that returns the positions of the team at this moment
@app.get('/positions')
def get_positions():
    try:
        return JBase.get_positions()
    except:
        return 'SORRY'
# If a 404 error occures return SORRY
@app.error(404)
def error404(error):
    return 'SORRY'
# If a 500 error occures return SORRY
@app.error(500)
def error500(error):
    return 'OK'
# RUN THE PACKETSERVER on 0.0.0.0/8080
app.run(host='0.0.0.0',port='8080',debug=True)
