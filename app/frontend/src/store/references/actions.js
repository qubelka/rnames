export const addRef = ref => (dispatch, getState) => {
	dispatch({
		type: 'ADD',
		ref,
	})
}

export const updateRef = ref => (dispatch, getState) => {
	dispatch({
		type: 'UPDATE',
		ref,
	})
}
