import * as React from 'react'
import { render } from 'react-dom'
import { Provider } from 'react-redux'
import { applyMiddleware, compose, createStore, StoreEnhancer } from 'redux'
import { offline } from '@redux-offline/redux-offline'
import offlineConfig from '@redux-offline/redux-offline/lib/defaults'
import { NetworkCallback } from '@redux-offline/redux-offline/lib/types'
import logger from 'redux-logger'
import thunk from 'redux-thunk'
import isReachable from 'is-reachable'

import { AppContainer } from 'blapp/commerce/containers/App'
import reducer from 'blapp/commerce/reducers'

const persistCallback = () => {
  doRender()
  store.subscribe(() => doRender())
}

const detectNetwork = (callback: NetworkCallback) => {
  const handle = (status: boolean) => {
    // Copy-ished from original redux-offline implementation
    if (window.requestAnimationFrame) {
      window.requestAnimationFrame(() => callback(status))
    } else {
      setTimeout(() => callback(status), 0)
    }
  }

  const checkNetwork = () => {
    if (navigator.onLine === false) {
      handle(false)
    }

    isReachable(location.origin, {timeout: 5000}).then(handle)
  }

  window.addEventListener("online", checkNetwork)
  window.addEventListener("offline", checkNetwork)
  setInterval(checkNetwork, 60000)
  checkNetwork()
}

const offlineConf = {
  ...offlineConfig,
  persistCallback,
  detectNetwork,
}

const store = createStore(
  reducer,
  compose(
    applyMiddleware(thunk),
    offline(offlineConf) as StoreEnhancer,
    applyMiddleware(logger),
  )
)

const placeholderElem = document.getElementById('APP_PLACEHOLDER')
const doRender = () => render(
  <Provider store={store}>
    <AppContainer />
  </Provider>,
  placeholderElem,
)
