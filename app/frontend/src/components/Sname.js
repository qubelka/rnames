import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { deleteSname } from '../store/snames/actions'
import { selectMap, selectRelations, selectNamesAddedByUser, selectLocationsAddedByUser } from '../store/snames/selectors'
import { deleteName } from '../store/names/actions'
import { deselectStructuredName } from '../store/selected_structured_names/actions'
import { formatStructuredName, parseId } from '../utilities'

const NAME_DELETE_ERROR_MSG =
	'The structured name you are trying to delete contains a recently created name, \
which is used in other structured names. If you want to delete this name, delete all the \
structured names containing it.'

const LOCATION_DELETE_ERROR_MSG =
	'The structured name you are trying to delete contains a recently created location, \
which is used in other structured names. If you want to delete this location, delete all the \
structured names containing it.'

export const Sname = ({ sname }) => {
	const dispatch = useDispatch()
	const map = useSelector(selectMap)
	const relations = useSelector(selectRelations)
	const snameNames = useSelector(state => selectNamesAddedByUser(state, sname.id))
	const snameLocations = useSelector(state => selectLocationsAddedByUser(state, sname.id))

	const deleteSnameHandler = () => {
		let canDelete = relations.every(rel => {
			if (rel.name1 === sname.id || rel.name2 === sname.id) {
				console.log(
					'Added relation is dependent on this sname. Please remove the relation associated with this sname first.'
				)
				return false
			}
			return true
		})

		let canDeleteName
		let canDeleteLocation

		if (parseId(sname.name_id).type === 'db_name') {
			canDeleteName = false
		} else {
			canDeleteName = snameNames.every(name => {
				if (name === sname.name_id) {
					console.log(NAME_DELETE_ERROR_MSG)
					return false
				}
				return true
			})
		}

		if (parseId(sname.location_id).type === 'db_location') {
			canDeleteLocation = false
		} else {
			canDeleteLocation = snameLocations.every(location => {
				if (location === sname.location_id) {
					console.log(LOCATION_DELETE_ERROR_MSG)
					return false
				}
				return true
			})
		}

		if (!canDelete) return
		if (canDeleteName) dispatch(deleteName(sname.name_id))
		if (canDeleteLocation) dispatch(deleteName(sname.location_id))
		dispatch(deselectStructuredName(sname.id))
		dispatch(deleteSname(sname))
	}

	return (
		<div>
			<button type='button' onClick={deleteSnameHandler}>
				Delete
			</button>
			<span>{formatStructuredName(sname, { map })}</span>
		</div>
	)
}
