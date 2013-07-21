
$().ready(function () {
    $('form').submit(function (e) {
        e.preventDefault();
        events.fetch({'data': $(e.currentTarget).serialize()});
    });
    
    $('#geo').click(function () {
        navigator.geolocation.getCurrentPosition(function(position) {
            events.fetch({'data': {'lat': position.coords.latitude, 'lon': position.coords.longitude }});
        });
    });
    
    var Event = Backbone.Model.extend({
        urlRoot: "/api/update",
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
        tagName: "li",
        className: "well",
        template: _.template($('#template_event').html()),
        events: {
          "click .food" : "toggle_food",
          "click .book" : "book"
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
        book: function () {
            window.location.href = this.model.get("url");
        },
        toggle_food: function () {
            this.model.toggle_food();
        }
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
            this.$el.append(view.render().el);
        }
    });
    
    var events_view = new EventsView;
});


