
$().ready(function () {
    _.extend(oevents, Backbone.Events);
    
    // Setting up forms
    $('form').submit(function (e) {
        e.preventDefault();
        data = $(e.currentTarget).serialize()
        if (data == "location=") {
            data = "location=London%2C+UK"
        }
        events.fetch({'data': data});
        $("#events").append("<li>Getting results...<li>")
    });
    
    $('#geo').click(function () {
        navigator.geolocation.getCurrentPosition(function(position) {
            events.fetch({'data': {'lat': position.coords.latitude, 'lon': position.coords.longitude }});
        });
    });
    
    // Backbone Events
    oevents.on("update", function (this_event) {
        var popup = new PopupView({
            model: this_event
        });
        
        if (this_event.get("has_food")) {
            popup.render(
                "Change event?",
                "Are you sure you wish to mark that " + this_event.get("title") + " <b> has no free food?</b>",
                "Save change",
                this_event.toggle_food
            )
        }
        else {            
            popup.render(
                "Change event?",
                "Are you sure you wish to mark that " + this_event.get("title") + " <b>has having free food?</b>",
                "Save change",
                this_event.toggle_food
            )
        }
    });
    
    // Backbone MVC
    
    var Event = Backbone.Model.extend({
        urlRoot: "/api/update",
        toggle_food: function (model) {
            that = model || this
            that.save({food: !that.get('food')});
        },
        no_food: function (model) {
            that = model || this
            that.save({food: false});
        },
        has_food: function (model) {
            that = model || this
            that.save({food: true});
        },
    });
    
    var EventView = Backbone.View.extend({
        tagName: "li",
        className: "well",
        template: _.template($('#template_event').html()),
        events: {
          "click .book" : "book",
          "click .food" : "toggle_food",
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
            oevents.trigger("update", this.model);
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
                throw("Returned data failed: " + response.message);
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
    
    var PopupView = Backbone.View.extend({
        template: _.template($('#template_popup').html()),
        events: {
          "click .ok" : "ok",
          "click .cancel" : "cancel"
        },
        render: function(title, content, button_label, success) {
            this.success = success
            this.$el.html(
                this.template({'title': title, 'content': content, 'button_label': button_label})
            );
            $('body').append(this.$el);
            this.popup = $(this.$el.children()[0]);
            this.popup.modal('show');
        },
        hide: function() {
            this.popup.modal('hide');
        },
        ok: function () {
            this.success(this.model);
            this.hide();
        },
        cancel: function () {
            this.hide();
        }
    });
});

var oevents = {};


