
import webapp2

from appengine_config import SESSION_SECRET_KEY

from webapp2_extras import routes
from webapp2 import Route as r

from controllers.ngo import NgoHandler, TwoPercentHandler, TwoPercent2Handler, DonationSucces


config = {
    'webapp2_extras.auth': {
        'user_model': 'models.user.User',
        'user_attributes': ['first_name']
    },
    # by default the session backend is the cookie
    # cookie_name: session
    # session_max_age: None => until the client is closed
    'webapp2_extras.sessions': {
        'secret_key': SESSION_SECRET_KEY
    }
}

# use string in dotted notation to be lazily imported
app = webapp2.WSGIApplication([
        # the public part of the app
        r('/',          handler="controllers.site.HomePage"),
        r('/despre',    handler="controllers.site.AboutHandler"),

        r('/termeni',    handler="controllers.site.TermsHandler"),
        r('/politica',   handler="controllers.site.PolicyHandler"),

        # account management
        r('/cont-nou',  handler="controllers.account_management.SignupHandler"),
        r('/login',     handler="controllers.account_management.LoginHandler", name='login'),
        r('/logout',    handler="controllers.account_management.LogoutHandler", name='logout'),

        r('/forgot',    handler="controllers.account_management.ForgotPasswordHandler", name='forgot'),
        r('/password',  handler="controllers.account_management.SetPasswordHandler"),
        # verification url: used for signup, and reset password
        r('/<type:v|p>/<user_id:\d+>-<signup_token:.+>', handler="controllers.account_management.VerificationHandler", name='verification'),
        
        # my account
        r('/contul-meu',        handler="controllers.my_account.MyAccountHandler", name='contul-meu'),
        r('/asociatia',         handler="controllers.my_account.NgoDetailsHandler", name='asociatia'),
        r('/date-cont',         handler="controllers.my_account.MyAccountDetailsHandler", name='date-contul-meu'),

        r('/api/check-ngo-api/<ngo_url>', handler="controllers.api.CheckNgoUrl", name='api-check-ngo-url'),

        # ADMIN HANDLERS
        r('/admin',             handler="controllers.admin.AdminHandler",       name='admin'),
        r('/admin/ong-nou',     handler="controllers.admin.AdminNewNgoHandler", name='admin-ong-nou'),
        r('/admin/<ngo_url>',   handler="controllers.admin.AdminNgoHandler",    name='admin-ong'),


        r('/<ngo_url>',         handler=NgoHandler, name="ngo-url"),
        r('/catre/<ngo_url>',   handler=NgoHandler),

        r('/<ngo_url>/doilasuta',           handler=TwoPercentHandler),
        r('/<ngo_url>/doilasuta/pas-2',     handler=TwoPercent2Handler),
        r('/<ngo_url>/doilasuta/succes',    handler=DonationSucces,     name="ngo-twopercent-success"),

    ],
    debug=True,
    config=config
)
