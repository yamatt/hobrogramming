
$().ready(function () {
    $('form').submit(function (e) {
        e.preventDefault();
        events.fetch({'data': $(e.currentTarget).serialize()});
    });
    
    var Event = Backbone.Model.extend({
        toggle_food: function () {
            this.save({food: !this.get('food')});
        },
        no_food: function () {
            this.save({food: false});
        },
        has_food: function () {
            this.save({food: true});
        },
    });
    
    var EventView = Backbone.View.extend({
        template: _.template($('#template_event').html()),
        events: {
          "click .food"   : "toggle_food",
          "click .boot"  : "mark_book"
        },
        initialize: function() {
            this.listenTo(this.model, 'change', this.render);
        },
        render: function() {
            this.$el.html(
                this.template({
                    event: this.model.toJSON()
                })
            );
            return this;
        },
    });
    
    var Events = Backbone.Collection.extend({
        model: Event,
        url: "/api/get",
        parse: function(response){
            if (response.events) {
                return response.events;
            }
            else {
                throw("Returned data failed: " + response);
            }
        }
    });
    
    var events = new Events;
    
    var EventsView = Backbone.View.extend({
        el: $('#events'),
        initialize: function() {
            this.listenTo(events, 'sync', this.render);
        },
        render: function () {
            var that = this;
            this.$el.empty();
            events.each(function(event) {
                that.add(event);
            });
        },
        add: function (event) {
            var view = new EventView({model:event});
            this.$el.prepend(view.render().el);
        }
    });
});


