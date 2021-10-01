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

const idTypes = [
	`name`,
	`location`,
	`qualifier`,
	`structured_name`,
	`reference`,
	`relation`,
	`db_name`,
	`db_location`,
	`db_qualifier_name`,
	`db_qualifier`,
	`db_structured_name`,
	`db_reference`
]

let ID = 0;

export const parseId = id => JSON.parse(id)

export const makeId = (ty, value) => {
	if (!idTypes.includes(ty))
		throw new Error(`Id type must not be one of allowed types, was "${ty}"`)

	const id = value === undefined ? ID++ : Number(value)
	const idString = JSON.stringify({type: ty, value: id})
	return idString
}

export default store