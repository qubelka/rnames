export const addRel = rel => (dispatch, getState) => {
	dispatch({
		type: 'ADD',
		rel,
	})
}

export const updateRel = rel => (dispatch, getState) => {
	dispatch({
		type: 'UPDATE',
		rel,
	})
}
