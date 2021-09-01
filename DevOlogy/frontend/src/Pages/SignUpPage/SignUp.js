import React, { Component } from "react";
import "./Signup.css";

export default class SignUp extends Component {
  render() {
    return (
        <div>
        <div className="container">
        <div className="white-box flex-h-center" id='main'>
            <div className="container-fluid logo-c flex-h-center">
                <img id="logo" src="{% static 'images/written-logo.png' %}" alt=""/>
            </div>
            <div className="err"><span id="err"></span></div>
            <div className="container-fluid form flex-h-center">
                <form method="post" className="container-fluid form flex-h-center">
                    <div className="container-fluid flex-v-center"> <input id="email" type="email" name="email"
                            placeholder="Email" className="form-content" onFocus="this.placeholder = ''"
                            onBlur="this.placeholder='Email'"/>
                        <div className="form-content-err" id='email-err'><img  src="{% static 'images/error.png' %}" width="100%"/></div>
                    </div>
                    <div className="container-fluid flex-v-center"> <input id="username" type="tect" name="username"
                            placeholder="Username" className="form-content" onFocus="this.placeholder = ''"
                            onBlur="this.placeholder='Username'"/>
                        <div className="form-content-err" id='username-err'><img  src="{% static 'images/error.png' %}" width="100%"/></div>
                    </div>
                    <div className="container-fluid flex-v-center"> <input id="name" type="text" name="full_name"
                            placeholder="Name" className="form-content" onFocus="this.placeholder = ''"
                            onBlur="this.placeholder='Name'"/>
                            <div className="form-content-err" id='name-err'><img /></div>
                    </div>
                    <div className="container-fluid flex-v-center"> <input type="password" name="password"
                            placeholder="Password" className="form-content" onFocus="this.placeholder = ''"
                            onBlur="this.placeholder='Password'" id="password"/>
                        <div  id='pass-err' className="form-content-err"><img src="{% static 'images/error.png' %}" width="100%"/></div>
                    </div>
                    <button type="submit" className="btn btn-primary form-content" id="sub-btn">Sign Up</button>
                </form>
            </div>
            <div className="container-fluid extras">
                <div className="row mt-2">
                    <div className="col-5 flex-v-center">
                        <hr width="100%"/>
                    </div>
                    <div className="col-2 flex-v-center" style="text-align: center;">OR</div>
                    <div className="col-5 flex-v-center">
                        <hr width="100%"/>
                    </div>
                </div>
                <div className="fb-btn flex-v-center">
                    <a className="form-content" href="{% url 'social:begin' 'facebook' %}"><button
                            className="btn btn-primary">Login with
                            Facebook
                        </button></a>
                </div>

            </div>
        </div>
        <div className="white-box flex-h-center" style="text-align: center;" id="signup">
            <div>Already have an Account ? <a href="/auth/login" className="normalize-link"
                    style="margin-left: 8px;">Log In</a></div>
        </div>
    </div>
    </div>
    
    );
  }
}
