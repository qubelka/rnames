import { createStore, combineReducers, applyMiddleware } from 'redux'
import thunk from 'redux-thunk'
import { composeWithDevTools } from 'redux-devtools-extension'
import { refReducer } from './references/reducers'
import { snameReducer } from './snames/reducers'
import { relReducer } from './relations/reducers'
import { mapReducer } from './map/reducers'

const devTools =
	process.env.NODE_ENV === 'production'
		? applyMiddleware(thunk)
		: composeWithDevTools(applyMiddleware(thunk))

export const store = createStore(
	combineReducers({
		ref: refReducer,
		sname: snameReducer,
		rel: relReducer,
		map: mapReducer
	}),
	devTools
)

export const mapId = (key, value) => (dispatch, getState) => {
	dispatch({
		type: 'MAP_VALUE',
		key,
		value
	})
}

export const initMapvalues = map => (dispatch, getState) => {
	dispatch({
		type: 'INITIALIZE_MAP_VALUES',
		map
	})
}

export const addName = (refId, name) => (dispatch, getState) => {
	dispatch({
		type: 'ADD_NAME',
		refId,
		name
	})
}

export const updateName = (refId, name, nameId) => (dispatch, getState) => {
	dispatch({
		type: 'UPDATE_NAME',
		refId,
		name,
		nameId
	})
}

export const addRef = ref => (dispatch, getState) => {
	dispatch({
		type: 'ADD',
		ref
	})
}

export const updateRef = ref => (dispatch, getState) => {
	dispatch({
		type: 'UPDATE',
		ref
	})
}

export const addSname = sname => (dispatch, getState) => {
	dispatch({
		type: 'ADD',
		sname
	})
}

export const updateSname = sname => (dispatch, getState) => {
	dispatch({
		type: 'UPDATE',
		sname
	})
}

export const addRel = rel => (dispatch, getState) => {
	dispatch({
		type: 'ADD',
		rel
	})
}

export const updateRel = rel => (dispatch, getState) => {
	dispatch({
		type: 'UPDATE',
		rel
	})
}

export default store