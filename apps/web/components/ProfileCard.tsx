type Props = { name: string; photoUrl: string; mockupUrl?: string; privateView?: boolean; goals?: string[] };
export default function ProfileCard({ name, photoUrl, mockupUrl, privateView, goals=[] }: Props) {
  const image = mockupUrl || photoUrl;
  return (
    <div style={{ borderRadius: 16, border: '1px solid #ddd', overflow: 'hidden', maxWidth: 420 }}>
      <img src={image} alt={name} style={{ width: '100%', display: 'block' }} />
      <div style={{ padding: 16, background: '#2E8B57', color: 'white' }}>
        <strong>{name}</strong>
      </div>
      {privateView && (
        <div style={{ padding: 16, background: 'white' }}>
          <ul>
            {goals.map((g, i) => (<li key={i}>{g}</li>))}
          </ul>
          <button style={{ background:'#FF4500', color:'#fff', border:'none', padding:'10px 12px', borderRadius:8 }}>
            Update Goals
          </button>
        </div>
      )}
    </div>
  );
}
