export const addSname = sname => (dispatch, getState) => {
	dispatch({
		type: 'ADD',
		sname,
	})
}

export const updateSname = sname => (dispatch, getState) => {
	dispatch({
		type: 'UPDATE',
		sname,
	})
}
