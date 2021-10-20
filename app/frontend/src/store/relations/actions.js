import { ADD, UPDATE } from '../action-types'

export const addRel = rel => {
	return {
		type: ADD,
		rel,
	}
}

export const updateRel = rel => {
	return {
		type: UPDATE,
		rel,
	}
}
