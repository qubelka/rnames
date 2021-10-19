export const snameReducer = (state = [], { type, sname }) => {
	if (sname === undefined) return state
	let ret = null

	switch (type) {
		case 'ADD':
			ret = state.concat(sname)
			break
		case 'UPDATE':
			ret = state.map(v => (v.id === sname.id ? sname : v))
			break
		default:
			ret = state
			break
	}

	return ret
}
