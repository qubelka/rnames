import React from 'react'
import { Notification } from './Notification'

export const InputField = ({ name, value, notification, setField }) => {
	return (
		<>
			<label htmlFor={name}>{name}</label>
			<input
				type='text'
				name={name}
				value={value}
				onChange={e => setField(e.target.value)}
			/>
			<Notification notification={notification} />
			<br />
		</>
	)
}
