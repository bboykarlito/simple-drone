#ifndef GAZEBO_PLUGINS_DRONE_SIMPLE_H
#define GAZEBO_PLUGINS_DRONE_SIMPLE_H

#include "gazebo/physics/Link.hh"
#include "gazebo/physics/Model.hh"
#include "gazebo/physics/World.hh"
#include "sdf/sdf.hh"

#include "simple_drone_description/plugin_drone_private.h"


using namespace std::placeholders;

namespace gazebo_plugins
{

class DroneSimpleController : public gazebo::ModelPlugin
{
public:
  DroneSimpleController(void);
  virtual ~DroneSimpleController(void);

protected:
  virtual void Load(gazebo::physics::ModelPtr _model, sdf::ElementPtr _sdf);
  virtual void Update(const gazebo::common::UpdateInfo & _info);
  virtual void Reset(void);

private:
  std::unique_ptr<DroneSimpleControllerPrivate> impl_;  // Forward declaration of pimpl idiom

  gazebo::event::ConnectionPtr updateConnection; // Pointer to the update event connection

  /// \brief The parent World
  gazebo::physics::WorldPtr world;

  /// \brief The link referred to by this plugin
  gazebo::physics::LinkPtr link;
  std::string link_name_;

  /// \brief save last_time
  gazebo::common::Time last_time;
};

}

#endif // GAZEBO_PLUGINS_DRONE_SIMPLE_H
