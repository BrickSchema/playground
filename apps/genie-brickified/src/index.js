import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import { Router } from 'react-router-dom';
import { createHashHistory } from 'history';
import { CookiesProvider } from 'react-cookie';

const history = createHashHistory();

ReactDOM.render((
    <Router history={history}>
        <CookiesProvider>
            <App />
        </CookiesProvider>
    </Router>
), document.getElementById('root'));
