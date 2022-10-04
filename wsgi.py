"""Web Server Gateway Interface"""

##################
# FOR PRODUCTION
####################
import src.app as app

if __name__ == "__main__":
    ####################
    # FOR DEVELOPMENT
    ####################
    app.run(host='0.0.0.0', debug=True)