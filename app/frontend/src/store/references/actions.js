import { ADD, UPDATE } from '../action-types'

export const addRef = ref => {
	return {
		type: ADD,
		ref,
	}
}

export const updateRef = ref => {
	return {
		type: UPDATE,
		ref,
	}
}
