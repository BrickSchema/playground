import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import { Router } from 'react-router-dom';
import { createBrowserHistory } from 'history';
import { CookiesProvider } from 'react-cookie';

const history = createBrowserHistory();

ReactDOM.render((
    <Router history={history}>
        <CookiesProvider>
            <App />
        </CookiesProvider>
    </Router>
), document.getElementById('root'));
