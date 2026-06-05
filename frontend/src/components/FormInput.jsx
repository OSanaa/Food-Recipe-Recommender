export default function FormInput({ label, type = "text", ...props }) {
    return (
        <div>
            <label className="block text-sm font-medium mb-1">{label}</label>
            {type === "textarea" ? (
                <textarea className="w-full px-3 py-2 border rounded text-sm" rows={4} {...props} />
            ) : (
                <input className="w-full px-3 py-2 border rounded text-sm" type={type} {...props} />
            )}
        </div>
    )
}