import { createStore, combineReducers, applyMiddleware } from 'redux'
import thunk from 'redux-thunk'

const refReducer = (state = [], {type, ref}) => {
	if (ref === undefined) return state
	let ret = null

	switch (type) {
		case `ADD`: ret = [...state, ref]; break
		case `UPDATE`: ret = state.map(v => v.id === ref.id ? ref : v); break
		default: ret = state; break
	}

	return ret
}

const idReducer = (state = 0, {type, id}) => {
	if (id === undefined) return state

	return state + 1
}

const snameReducer = (state = [], {type, sname}) => {
	if (sname === undefined) return state
	let ret = null

	switch (type) {
		case `ADD`: ret = state.concat(sname); break
		case `UPDATE`: ret = state.map(v => v.id === sname.id ? sname : v); break
		default: ret = state; break
	}

	return ret
}

const relReducer = (state = [], {type, rel}) => {
	if (rel === undefined) return state
	let ret = null

	switch (type) {
		case `ADD`: ret = state.concat(rel); break
		case `UPDATE`: ret = state.map(v => v.id === rel.id ? rel : v); break
		default: ret = state; break
	}

	return ret
}

export const store = createStore(
	combineReducers({
		ref: refReducer,
		id: idReducer,
		sname: snameReducer,
		rel: relReducer
	}),
	applyMiddleware(thunk)
)

export const addRef = ref => (dispatch, getState) => {
	dispatch({
		type: `ADD`,
		ref
	})
}

export const updateRef = ref => (dispatch, getState) => {
	dispatch({
		type: `UPDATE`,
		ref
	})
}

export const addSname = sname => (dispatch, getState) => {
	dispatch({
		type: `ADD`,
		sname
	})
}

export const updateSname = sname => (dispatch, getState) => {
	dispatch({
		type: `UPDATE`,
		sname
	})
}

export const addRel = rel => (dispatch, getState) => {
	dispatch({
		type: `ADD`,
		rel
	})
}

export const updateRel = rel => (dispatch, getState) => {
	dispatch({
		type: `UPDATE`,
		rel
	})
}

export const getId = () => {
	const id = store.getState().id

	store.dispatch({
		type: `INCREMENT`,
		id
	})

	return id
}

export default store