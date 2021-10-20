import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { loadServerData } from '../services/server'
import { formatQualifier } from '../utilities'
import { updateSname } from '../store/snames/actions'
import { Dropdown } from './Dropdown'

export const Sname = ({ data }) => {
	const dispatch = useDispatch()
	const state = useSelector(v => v)
	const referenceData = state.ref
	const refs = referenceData.reduce(
		(p, c) =>
			p.concat(
				...c.names.map(v => {
					return { ...v, refId: c.id }
				})
			),
		[]
	)

	const names = refs
		.filter(v => v.variant === 'name')
		.concat(...loadServerData('names'))
		.map(v => [v.id, v.name])

	const qualifiers = refs
		.filter(v => v.variant === 'qualifier')
		.concat(...loadServerData('qualifiers'))
		.map(v => [v.id, formatQualifier(v, state)])

	const locations = refs
		.filter(v => v.variant === 'location')
		.concat(...loadServerData('locations'))
		.map(v => [v.id, v.name])

	const references = referenceData
		.concat(...loadServerData('references'))
		.map(v => [v.id, v.title])

	const update = ({ target }, field) => {
		const r = { ...data }
		r[field] = target.value
		dispatch(updateSname(r))
	}

	return (
		<div>
			<label htmlFor='name'>Name</label>
			<Dropdown
				name='name'
				options={names}
				value={data.name}
				onChange={e => update(e, 'name_id')}
			/>
			<br />
			<label htmlFor='qualifier'>Qualifier</label>
			<Dropdown
				name='qualifier'
				options={qualifiers}
				value={data.qualifier}
				onChange={e => update(e, 'qualifier_id')}
			/>
			<br />
			<label htmlFor='location'>Location</label>
			<Dropdown
				name='location'
				options={locations}
				value={data.location}
				onChange={e => update(e, 'location_id')}
			/>
			<br />
			<label htmlFor='reference'>Reference</label>
			<Dropdown
				name='reference'
				options={references}
				value={data.reference_id}
				onChange={e => update(e, 'reference_id')}
			/>
		</div>
	)
}
