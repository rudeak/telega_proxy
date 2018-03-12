import app

def edit_game_name (id, name):
    game = Game.query.filter_by (game_id = id).first()
    game.game_name = name
    print ('new game name ='+ name)
    try:
        print (game.game_name)
        db.session.commit()
        return 1
    except:
        db.session.rollback()
        return 'помилка редагування назви гри'