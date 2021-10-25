export const relReducer = (state = [], { type, rel }) => {
	if (rel === undefined) return state
	let ret = null

	switch (type) {
		case 'ADD':
			ret = state.concat(rel)
			break
		case 'UPDATE':
			ret = state.map(v => (v.id === rel.id ? rel : v))
			break
		default:
			ret = state
			break
	}

	return ret
}