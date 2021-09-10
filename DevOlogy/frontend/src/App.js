import ReactDOM from "react-dom";
import React, { Component } from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import regeneratorRuntime from "regenerator-runtime";
import Feed from "./Pages/Feed/Feed";
import Login from "./Pages/LoginPage/Login";
import Profile from "./Pages/Profile/Profile";
import SignUp from "./Pages/SignUpPage/SignUp";
import { syncFetchRequest } from "../helpers/fetchRequest";
import SingleTonPost from './Pages/SingleTonPost/SingleTonPost.js'
class App extends Component {
  constructor() {
    super();
    this.state = { isLoggedIn: false };
    this.knowIfLoggedIn = this.knowIfLoggedIn.bind(this);
  }
  UNSAFE_componentWillMount() {
    this.knowIfLoggedIn();
  }
  knowIfLoggedIn() {
    syncFetchRequest({
      path_: "/api/isLoggedIn/",
      method: "POST",
      next: (data) => {
        this.setState({ isLoggedIn: data.result === "True" ? true : false });
      },
    });
  }

  render() {
    return (
      <Router>
        <Switch>
          <Route exact path="/">
            <Feed />
          </Route>
          <Route exact path="/post/:postId">
            <SingleTonPost/>
          </Route>
          <Route exact path="/profile/:userId">
            <Profile />
          </Route>

          <Route exact path="/login">
            <Login />
          </Route>
          <Route exact path="/signup">
            <SignUp />
          </Route>
        </Switch>
      </Router>
    );
  }
}

ReactDOM.render(<App />, document.getElementById("app"));
export default App;
