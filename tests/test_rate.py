def test_post(client):
    response = client.post('/rate', json={
        
        "title": "TESTE API",
        "content": "CONTEÚDO",
        "rate_type": "Anime",
        "rate": 4
    
    })
    assert 'TESTE API' in response.json['title']
    
def test_get(client):
    response = client.get('/rate')
    assert len(response.json) == 1