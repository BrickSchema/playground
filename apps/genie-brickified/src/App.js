import React, { Component } from 'react';
import './App.css';
import Home from './client/Homepage';
import Main from './client/Mainpage';
import {
  HashRouter as Router,
  Route,
  Switch,
} from 'react-router-dom';
import {
    LOGIN_URL
} from './config'

class App extends Component {
  render() {
    var params = new URL(document.location).searchParams;
    var token = params.get("token");
    if (token) {
      window.sessionStorage.setItem("token", token);
    }

    return (
      <Router>
        <div>
          <Switch>
            <Route exact path="/" component={Home} />
            <Route path="/main" component={Main} />
            <Route path='/login' component={() => {
                window.location.href = LOGIN_URL;
                return null;
            }}/>
          </Switch>
        </div>
      </Router>
    );
  }
}

export default App;
