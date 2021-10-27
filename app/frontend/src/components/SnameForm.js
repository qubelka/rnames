import React, { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { formatQualifier } from '../utilities'
import { parseId, makeId } from '../utilities'
import { addName } from '../store/names/actions'
import { addSname } from '../store/snames/actions'
import { Datalist } from './Datalist'

export const SnameForm = () => {
	const dispatch = useDispatch()
	const state = useSelector(v => v)

	const [name, setName] = useState('')
	const [location, setLocation] = useState('')
	const [qualifier, setQualifier] = useState('')
	const [reference, setReference] = useState('')

	const names = useSelector(v => {
		return Object.entries(v.map)
			.filter(([key]) => parseId(key).type === 'db_name')
			.map(v => [v[1].id, v[1].name])
			.concat(
				v.names
					.filter(name => name.variant === 'name')
					.map(v => [v.id, v.name])
			)
	})

	const qualifiers = useSelector(v => {
		return Object.entries(v.map)
			.filter(([key]) => parseId(key).type === 'db_qualifier')
			.map(v => [v[1].id, formatQualifier(v[1], state)])
	})

	const locations = useSelector(v => {
		return Object.entries(v.map)
			.filter(([key]) => parseId(key).type === 'db_location')
			.map(v => [v[1].id, v[1].name])
			.concat(
				v.names
					.filter(name => name.variant === 'location')
					.map(v => [v.id, v.name])
			)
	})

	const references = useSelector(v => {
		return Object.entries(v.map)
			.filter(([key]) => parseId(key).type === 'db_reference')
			.map(v => [v[1].id, v[1].title])
			.concat(v.ref.map(ref => [ref.id, ref.title]))
	})

	const handleSnameAddition = () => {
		const qualifierFromDb = qualifiers.find(
			dbQualifier => dbQualifier[1] === qualifier
		)
		const referenceFromDb = references.find(
			dbReference => dbReference[1] === reference
		)

		if (!qualifierFromDb || !referenceFromDb) return

		let nameId, locationId
		if (names.filter(v => v[1] === name).length === 0) {
			nameId = makeId('name')
			dispatch(addName({ id: nameId, name: name, variant: 'name' }))
		}

		if (locations.filter(v => v[1] === location).length === 0) {
			locationId = makeId('location')
			dispatch(
				addName({ id: locationId, name: location, variant: 'location' })
			)
		}

		const newSname = {
			id: makeId('structured_name'),
			name_id: nameId || names.find(dbName => dbName[1] === name)[0],
			location_id:
				locationId ||
				locations.find(dbLocation => dbLocation[1] === location)[0],
			qualifier_id: qualifierFromDb[0],
			reference_id: referenceFromDb[0],
			remarks: '',
		}
		dispatch(addSname(newSname))
		setName('')
		setQualifier('')
		setLocation('')
		setReference('')
	}

	return (
		<div>
			<label htmlFor='name'>Name</label>
			<Datalist
				name='name'
				options={names}
				value={name}
				onChange={e => setName(e.target.value)}
			/>
			<br />
			<label htmlFor='qualifier'>Qualifier</label>
			<Datalist
				name='qualifier'
				options={qualifiers}
				value={qualifier}
				onChange={e => setQualifier(e.target.value)}
			/>
			<br />
			<label htmlFor='location'>Location</label>
			<Datalist
				name='location'
				options={locations}
				value={location}
				onChange={e => setLocation(e.target.value)}
			/>
			<br />
			<label htmlFor='reference'>Reference</label>
			<Datalist
				name='reference'
				options={references}
				value={reference}
				onChange={e => setReference(e.target.value)}
			/>
			<button type='button' onClick={handleSnameAddition}>
				Save
			</button>
		</div>
	)
}
