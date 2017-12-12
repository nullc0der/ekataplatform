import { compose, createStore, applyMiddleware} from 'redux'
import thunk    from 'redux-thunk'
import { routerMiddleware } from 'react-router-redux'
import throttle from 'lodash/throttle'
import rootReducer from './rootReducer'

export function storageSupported(){
  var testKey = 'ls-test';
  try {
    window.localStorage.setItem(testKey, '1');
    window.localStorage.removeItem(testKey);
    return true
  } catch (err){
    return false
  }
}

export function saveState(state){
  try {
    var serialized = JSON.stringify(state)
    localStorage.setItem('state', serialized)
  } catch (err){
    return undefined
  }
}

export function loadState(state){
  console.log('Loading persisted state...')
  try{
    var serialized = localStorage.getItem('state')
    if (serialized === null){
      return undefined
    }
    return JSON.parse(serialized)
  } catch (err){
    return undefined
  }
}


export default function configureStore(INITIAL_STATE={}, history){
  
  var middlewares = [
    applyMiddleware(thunk, routerMiddleware(history)) 
  ];

  if (__DEV__ && !__SERVER__)
    middlewares.push( window.devToolsExtension ? window.devToolsExtension() : (f)=> f )

  var store = createStore(
    rootReducer,
    INITIAL_STATE,
    compose(...middlewares)
  );


  if (module.hot) {
    module.hot.accept('./rootReducer', () => {
      store.replaceReducer(rootReducer);
    });
  }
  
  return store;
};