import ReactDOM from "react-dom";
import React, { Component } from "react";
import { BrowserRouter as Router, Route, Switch, Redirect } from "react-router-dom";
import regeneratorRuntime from "regenerator-runtime";
import Feed from "./Pages/Feed/Feed";
import Login from "./Pages/LoginPage/Login";
import Post from "./Pages/Post/Post";
import Profile from "./Pages/Profile/Profile";
import SignIn from "./Pages/SignInPage/SignIn";

class App extends Component {
  constructor() {
    super();
    this.state = { isLoggedIn: false };
    this.knowIfLoggedIn = this.knowIfLoggedIn.bind(this);
    this.knowIfLoggedIn();
  }
  async knowIfLoggedIn() {
    await fetch("/api/isLoggedIn", {
      headers:{
          'Accept': 'application/json',
          'X-Requested-With': 'XMLHttpRequest', }})
      .then((response) => {
        return response.json();
      })
      .then((json) => {
        this.setState({ isLoggedIn: json.result === "True" ? true : false });
      });
  }

  render() {
    return (
        <Router>
          { this.state.isLoggedIn ? 
            <div className="content">
              <Switch>
                <Route exact path="">
                  <Feed />
                </Route>
                <Route path="/post/:postId">
                  <Post />
                </Route>
                <Route path="/profile/:userId">
                  <Profile />
                </Route>
              </Switch>
            </div>
          
          :
          
            <div className="content">
              <Switch>
                <Route exact path="">
                  <Login />
                </Route>
                <Route path="/post/:postId">
                  <Login />
                </Route>
                <Route path="/post">
                  <Login/>
                </Route>
                <Route path="/signin">
                  <SignIn />
                </Route>
              </Switch>
            </div>
          }
        </Router>
    );
  }
}

ReactDOM.render(<App />, document.getElementById("app"));
export default App;
