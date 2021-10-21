import { ADD, UPDATE } from '../action-types'

export const addSname = sname => {
	return {
		type: ADD,
		sname,
	}
}

export const updateSname = sname => {
	return {
		type: UPDATE,
		sname,
	}
}
