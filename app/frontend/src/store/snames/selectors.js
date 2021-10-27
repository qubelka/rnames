import { createSelector } from 'reselect'
import { parseId } from '../../utilities'

export const selectDbNames = state => {
	return Object.entries(state.map).filter(
		([key]) => parseId(key).type === 'db_name'
	)
}

export const selectNames = state => {
	return state.names.filter(name => name.variant === 'name')
}

export const selectAllNames = createSelector(
	[selectDbNames, selectNames],
	(dbNames, names) => {
		return dbNames
			.map(v => [v[1].id, v[1].name])
			.concat(names.map(v => [v.id, v.name]))
	}
)

export const selectDbLocations = state => {
	return Object.entries(state.map).filter(
		([key]) => parseId(key).type === 'db_location'
	)
}

export const selectLocations = state => {
	return state.names.filter(name => name.variant === 'location')
}

export const selectAllLocations = createSelector(
	[selectDbLocations, selectLocations],
	(dbLocations, locations) => {
		return dbLocations
			.map(v => [v[1].id, v[1].name])
			.concat(locations.map(v => [v.id, v.name]))
	}
)

export const selectDbReferences = state => {
	return Object.entries(state.map).filter(
		([key]) => parseId(key).type === 'db_reference'
	)
}

export const selectRefence = state => {
	return state.ref
}

export const selectAllReferences = createSelector(
	[selectDbReferences, selectRefence],
	(dbReferences, reference) => {
		return dbReferences
			.map(v => [v[1].id, v[1].title])
			.concat(reference.map(ref => [ref.id, ref.title]))
	}
)
