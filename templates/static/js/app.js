async function load() {
  const res = await fetch('/api/items');
  const items = await res.json();
  const list = document.getElementById('list');
  list.innerHTML = '';
  items.forEach(i => {
    const li = document.createElement('li');
    li.textContent = `${i.name} — qty: ${i.quantity}`;
    list.appendChild(li);
  });
}
document.getElementById('addBtn').onclick = async () => {
  const name = document.getElementById('name').value;
  if (!name) return alert('enter name');
  await fetch('/api/items', {method:'POST', body:JSON.stringify({name}), headers:{'Content-Type':'application/json'}});
  document.getElementById('name').value='';
  load();
};
load();
